from __future__ import annotations
from abc import ABC, abstractmethod


# 抽象产品：按钮
class AbstractButton(ABC):
    @abstractmethod
    def paint(self):
        pass


# 抽象产品：文本框
class AbstractTextBox(ABC):
    @abstractmethod
    def paint(self):
        pass


# 具体产品：Windows按钮
class WindowsButton(AbstractButton):
    def paint(self):
        print("Painting Windows button")


# 具体产品：Windows文本框
class WindowsTextBox(AbstractTextBox):
    def paint(self):
        print("Painting Windows text box")


# 具体产品：Mac按钮
class MacButton(AbstractButton):
    def paint(self):
        print("Painting Mac button")


# 具体产品：Mac文本框
class MacTextBox(AbstractTextBox):
    def paint(self):
        print("Painting Mac text box")


# 抽象工厂
class GUIFactory(ABC):
    @abstractmethod
    def create_button(self) -> AbstractButton:
        pass

    @abstractmethod
    def create_text_box(self) -> AbstractTextBox:
        pass


# 具体工厂：Windows工厂
class WindowsFactory(GUIFactory):
    def create_button(self) -> AbstractButton:
        return WindowsButton()

    def create_text_box(self) -> AbstractTextBox:
        return WindowsTextBox()


# 具体工厂：Mac工厂
class MacFactory(GUIFactory):
    def create_button(self) -> AbstractButton:
        return MacButton()

    def create_text_box(self) -> AbstractTextBox:
        return MacTextBox()


# 客户端代码
def create_gui(factory: GUIFactory):
    button = factory.create_button()
    text_box = factory.create_text_box()
    button.paint()
    text_box.paint()


# 客户端使用
if __name__ == "__main__":
    print("Creating Windows GUI:")
    create_gui(WindowsFactory())
    print("\nCreating Mac GUI:")
    create_gui(MacFactory())
