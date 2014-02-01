import gevent, gevent.queue

MILLION = 1000 * 1000

def test_profiler():
    def foo():
        for i in range(20 * MILLION):
            if not i % MILLION:
                # Yield to the Gevent hub.
                gevent.sleep(0)

    def bar():
        for i in range(10 * MILLION):
            if not i % MILLION:
                gevent.sleep(0)

    foo_greenlet = gevent.spawn(foo)
    bar_greenlet = gevent.spawn(bar)
    foo_greenlet.join()
    bar_greenlet.join()

def test_whisper():
    in_ = gevent.queue.Channel()

    def whisper(src):
        return src.get() + 1

    out = in_
    for _ in range(1000):
        out = gevent.spawn(whisper, out)

    in_.put(1)
    print out.get()
