"""
模拟requests的timeout参数，使任意函数都拥有超时跳出的功能，防止访问超时阻塞影响代码的运行
"""
import functools
import signal


def with_timeout(timeout):
    """
    用法：设置timeout=超时秒数
    示例
    @with_timeout(5)
    def my_func():
        time.sleep(10)
        print("Function call finished")
    在这个示例中，my_func函数会休眠10秒钟，但是装饰器with_timeout(5)会限制函数的执行时间不超过5秒钟。
    如果函数在5秒钟内执行完成，那么装饰器不会起作用。但是如果函数在5秒钟内没有执行完成，那么会抛出TimeoutException异常。
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            def handler(signum, frame):
                raise print("Function call timed out after %s seconds" % timeout)
            # 设置SIGALRM信号的处理函数
            signal.signal(signal.SIGALRM, handler)
            # 在timeout秒后发送SIGALRM信号
            signal.alarm(timeout)
            try:
                result = func(*args, **kwargs)
            finally:
                # 取消SIGALRM信号
                signal.alarm(0)
            return result
        return wrapper
    return decorator
    

