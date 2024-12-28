import math
def distance_point(p1, p2):
    """两点间距离"""
    return math.sqrt((p1[0] - p2[0]) * (p1[0] - p2[0]) + (p1[1] - p2[1]) * (p1[1] - p2[1]))
class Circle_Colliders:
    """圆形碰撞体"""
    def __init__(self,obj):
        # 球形碰撞体半径和圆心
        self.center = obj.rect.center
        self.radius = (obj.rect.right - obj.rect.left) / 2

    def check_Colliders(self,other):
        """检测是否和 other 碰撞体接触"""
        return distance_point(self.center,other.center) <= (self.radius + other.radius)
