
mixins.py 里的 mixins（混入类，Mixin）是面向对象编程里的一个常见概念，主要用于 复用代码。

简单解释：

继承：子类继承父类，获得父类的功能；

Mixin：一种 局部功能模块，通常只提供一部分功能（比如日志、时间戳、分页、权限验证），然后“混入”到其它类里去用。

特点

不是完整的类：Mixin 本身通常不能单独实例化；

只实现某一方面的功能：比如排序、搜索、导出 Excel；

通过多继承组合：把一个或多个 Mixin 混入到业务类中，扩展功能；

比继承更灵活：避免“父类越来越臃肿”的问题。

举例（Django/DRF 里常见）
class LoggingMixin:
    def log(self, message):
        print(f"[LOG]: {message}")

class TimestampMixin:
    def set_timestamp(self):
        import datetime
        self.timestamp = datetime.datetime.now()

class MyModel(LoggingMixin, TimestampMixin):
    def save(self):
        self.set_timestamp()
        self.log("保存对象")
        print("对象已保存")

obj = MyModel()
obj.save()


这里：

LoggingMixin 提供日志功能；

TimestampMixin 提供时间戳功能；

MyModel 混入这两个功能后，不需要在一个类里写一大堆重复代码。

所以：
👉 mixins.py 文件一般就是放一些可复用的小功能类，供别的业务类继承组合用的。

 mixins.py 可能会写的常用功能清单（比如分页、缓存、日志、权限检查）
