import einops
import torch

import rust_circuit as rc


def test_a_samp_multinomial():
    weights = torch.rand(100)

    n_samp = 500
    k = 10
    my_counts = torch.zeros(weights.shape[0])
    torch_counts = torch.zeros(weights.shape[0])
    total_samp = 0
    for _ in range(100):
        repeated_weights = einops.repeat(weights, f"a -> {n_samp} a")
        torch_vals = torch.multinomial(repeated_weights, k)
        torch_counts.scatter_add_(
            0,
            torch_vals.flatten(),
            torch.ones_like(torch_vals).float().flatten(),
        )
        my_vals = rc.already_sampled_multinomial(
            rc.Array(weights), rc.Array(torch.empty_like(repeated_weights).exponential_()), shape=(k,)
        ).evaluate()
        my_counts.scatter_add_(
            0,
            my_vals.flatten(),
            torch.ones_like(my_vals).float().flatten(),
        )
        total_samp += n_samp
    torch_counts /= total_samp
    my_counts /= total_samp

    torch.testing.assert_close(my_counts, torch_counts, rtol=1e-1, atol=1e-2)
