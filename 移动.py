import tkinter as tk


class MovingNodeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("自动移动节点")

        # 创建画布
        self.canvas = tk.Canvas(root, width=600, height=400, bg="white")
        self.canvas.pack()

        # 创建节点
        self.node = self.canvas.create_oval(100, 100, 140, 140, fill="blue", tags="node")
        self.info_text = None
        self.direction = [2, 1.5]  # 节点移动的初始方向

        # 绑定鼠标事件
        self.canvas.tag_bind("node", "<Enter>", self.show_info)
        self.canvas.tag_bind("node", "<Leave>", self.hide_info)

        # 开始自动移动
        self.move_node()

    def move_node(self):
        """移动节点"""
        x1, y1, x2, y2 = self.canvas.coords(self.node)

        # 移动节点
        self.canvas.move(self.node, self.direction[0], self.direction[1])

        # 检测边界并改变方向
        if x1 <= 0 or x2 >= 600:
            self.direction[0] = -self.direction[0]
        if y1 <= 0 or y2 >= 400:
            self.direction[1] = -self.direction[1]

        # 每隔 30 毫秒重复移动
        self.root.after(30, self.move_node)

    def show_info(self, event):
        """显示节点信息"""
        if self.info_text is None:
            # 在节点上方显示信息
            x1, y1, x2, y2 = self.canvas.coords(self.node)
            self.info_text = self.canvas.create_text((x1 + x2) / 2, y1 - 10, text="节点1: 信息 A", fill="black")

    def hide_info(self, event):
        """隐藏节点信息"""
        if self.info_text:
            self.canvas.delete(self.info_text)
            self.info_text = None


if __name__ == "__main__":
    root = tk.Tk()
    app = MovingNodeApp(root)
    root.mainloop()
