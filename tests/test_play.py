# run tests with pytest --cov=jled tests/


from jled.play import play


def test_play_calls_update_until_done():
    class MockLed:
        def __init__(self, countdown):
            self.countdown = countdown

        def _update(self, _):
            self.countdown -= 1
            return self.countdown > 0

    led = MockLed(2)
    play(led)

    assert 0 == led.countdown
