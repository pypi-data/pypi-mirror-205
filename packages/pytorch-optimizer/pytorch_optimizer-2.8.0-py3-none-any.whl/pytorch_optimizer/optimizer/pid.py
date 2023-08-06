import torch
from torch.optim.optimizer import Optimizer

from pytorch_optimizer.base.exception import NoSparseGradientError
from pytorch_optimizer.base.optimizer import BaseOptimizer
from pytorch_optimizer.base.types import CLOSURE, DEFAULTS, LOSS, PARAMETERS


class PID(Optimizer, BaseOptimizer):
    r"""A PID Controller Approach for Stochastic Optimization of Deep Networks.

    :param params: PARAMETERS. iterable of parameters to optimize or dicts defining parameter groups.
    :param lr: float. learning rate.
    :param momentum: float. momentum factor.
    :param dampening: float. dampening for momentum.
    :param derivative: float. D part of the PID.
    :param integral: float. I part of the PID.
    :param weight_decay: float. weight decay (L2 penalty).
    :param weight_decouple: bool. the optimizer uses decoupled weight decay as in AdamW.
    """

    def __init__(
        self,
        params: PARAMETERS,
        lr: float = 1e-3,
        momentum: float = 0.0,
        dampening: float = 0.0,
        derivative: float = 10.0,
        integral: float = 5.0,
        weight_decay: float = 0.0,
        weight_decouple: bool = False,
    ):
        self.lr = lr
        self.momentum = momentum
        self.dampening = dampening
        self.derivative = derivative
        self.integral = integral
        self.weight_decay = weight_decay

        self.validate_parameters()

        defaults: DEFAULTS = {
            'lr': lr,
            'momentum': momentum,
            'dampening': dampening,
            'derivative': derivative,
            'integral': integral,
            'weight_decay': weight_decay,
            'weight_decouple': weight_decouple,
        }
        super().__init__(params, defaults)

    def validate_parameters(self):
        self.validate_learning_rate(self.lr)
        self.validate_momentum(self.momentum)
        self.validate_weight_decay(self.weight_decay)

    def __str__(self) -> str:
        return 'PID'

    @torch.no_grad()
    def reset(self):
        for group in self.param_groups:
            group['step'] = 0
            for p in group['params']:
                state = self.state[p]

                if group['momentum'] > 0.0:
                    state['grad_buffer'] = torch.zeros_like(p)
                    state['i_buffer'] = torch.zeros_like(p)
                    state['d_buffer'] = torch.zeros_like(p)

    @torch.no_grad()
    def step(self, closure: CLOSURE = None) -> LOSS:
        loss: LOSS = None
        if closure is not None:
            with torch.enable_grad():
                loss = closure()

        for group in self.param_groups:
            if 'step' in group:
                group['step'] += 1
            else:
                group['step'] = 1

            for p in group['params']:
                if p.grad is None:
                    continue

                grad = p.grad
                if grad.is_sparse:
                    raise NoSparseGradientError(str(self))

                state = self.state[p]

                if len(state) == 0 and group['momentum'] > 0.0:
                    state['grad_buffer'] = torch.zeros_like(p)
                    state['i_buffer'] = torch.zeros_like(p)
                    state['d_buffer'] = torch.zeros_like(p)

                if group['weight_decouple']:
                    p.mul_(1.0 - group['weight_decay'] * group['lr'])
                elif group['weight_decay'] > 0.0:
                    grad.add_(p, alpha=group['weight_decay'])

                if group['momentum'] > 0.0:
                    i_buf = state['i_buffer']
                    i_buf.mul_(group['momentum']).add_(grad, alpha=1.0 - group['dampening'])

                    g_buf, d_buf = state['grad_buffer'], state['d_buffer']
                    d_buf.mul_(group['momentum'])

                    if group['step'] > 1:
                        d_buf.add_(grad - g_buf, alpha=1.0 - group['momentum'])
                        g_buf.copy_(grad)

                    grad.add_(i_buf, alpha=group['integral']).add_(d_buf, alpha=group['derivative'])

                p.add_(grad, alpha=-group['lr'])

        return loss
