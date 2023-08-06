import os
import torch
from pathlib import Path


from mountaintop.core.internal.distribute import (
    get_local_rank,
)
from mountaintop.core.internal.module import import_module
from mountaintop.runx.trainer import Trainer
from mountaintop.runx.logx import loggerx
from mountaintop.utils.yaml import load_yaml

from mountaintop.bin.parser_base import (
    set_base_parser,
    add_arg_group
)


def set_export_parser(parser=None):
    if not parser:
        parser = set_base_parser()

    gp = add_arg_group(parser, 'export arguments')

    gp.add_argument('--config', required=True, help='config file')
    gp.add_argument('--checkpoint', required=True, help='checkpoint model')
    
    gp.add_argument(
        '--out', 
        required=True,
        help='export model destination'
    )

    gp.add_argument(
        '--quant',
        action='store_true',
        default=False,
        help='export quantized model'
    )
    
    gp.add_argument(
        '--verbose',
        action='store_true',
        default=False,
        help='output information'
    )

    gp.add_argument('--mode',
        choices=[
            'jit', 
        ],
        default='jit',
        help='export mode'
    )
    
    return parser


def remove_dropout(configs):
    for key, values in configs.items():
        if not isinstance(values, dict):
            continue
        for subkey, subvalue in values.items():
            if "dropout" in subkey:
                configs[key][subkey] = 0.0
    return


def run(args, unused_args):
    # No need gpu for model export
    os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

    configs = load_yaml(args.config)
    assert "model" in configs
    model_config = configs["model"]
    
    model_dir = os.path.dirname(args.checkpoint)
    # init magic logger
    loggerx.initialize(
        logdir=model_dir,
        to_file=False
    )
    local_rank = get_local_rank()
    loggerx.info(f"Local rank is {local_rank}")

    #################### init model
    # init model
    loggerx.info('Init model')
    assert "module" in model_config
    model_module_path = model_config.pop("module")
    model_module = import_module(model_module_path)
    remove_dropout(model_config)
    assert hasattr(model_module, "create_from_config"), \
        f"{model_module} should have init function [create_from_config]"
    model = model_module.create_from_config(model_config)
    loggerx.summary_model(model)
    
    trainer = Trainer(
        model=model,
        optimizer=None,
    )
    
    # If specify checkpoint, restore from checkpoint
    if args.checkpoint is not None:
        trainer.load_checkpoint(args.checkpoint, resume=False)
    
    # Export jit torch script model
    script_model = torch.jit.script(model)
    script_model.save(args.out)
    loggerx.info(f'Export model to {args.out}')

    # Export quantized jit torch script model
    if args.quant:
        quant_out = os.path.join(
            os.path.dirname(args.out), 
            f"{Path(args.out).stem}.qint8{os.path.splitext(args.out)[1]}"
        )
        quantized_model = torch.quantization.quantize_dynamic(
            model, {torch.nn.Linear}, dtype=torch.qint8
        )
        if args.verbose:
            loggerx.info(f"quantized_model:\n{quantized_model}")
        script_quant_model = torch.jit.script(quantized_model)
        script_quant_model.save(quant_out)
        loggerx.info(f'Export quantized model to {quant_out}')

