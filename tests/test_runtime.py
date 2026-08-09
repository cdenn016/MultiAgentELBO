from __future__ import annotations

from multiagent_elbo.runtime import RngStreams


def test_equal_seeds_produce_identical_named_stream_draws():
    first = RngStreams.from_seed(314159)
    second = RngStreams.from_seed(314159)

    for name in ("problem", "recognition", "controls", "figures"):
        assert getattr(first, name).integers(0, 2**31, size=8).tolist() == getattr(
            second, name
        ).integers(0, 2**31, size=8).tolist()


def test_named_streams_do_not_share_the_same_initial_draws():
    streams = RngStreams.from_seed(314159)

    draws = {
        name: tuple(getattr(streams, name).integers(0, 2**31, size=8))
        for name in ("problem", "recognition", "controls", "figures")
    }

    assert len(set(draws.values())) == 4
