import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.factory import Factory
from kivy.clock import Clock
from random import randint, random


class PongPaddle(Widget):
    score = NumericProperty(0)
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)
    
    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            offset = (ball.center_y-self.center_y)/(self.height/4)
            bounced = Vector(-1*vx, vy)
            vel = bounced * 1.1
            ball.velocity = vel.x, vel.y + offset   

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos

class PongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)
    
    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


class PongGame(Widget):
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)
    velo = (8,0)
    revel = (-8,0)

    def serve_ball(self, vel=velo):
        self.ball.center = self.center
        self.ball.velocity = vel
        
    def update(self, *args):
        self.ball.move()

        #bounce off paddles
        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)
        
        #stop the ball in case the position is within bounds
        self.player1.velocity_y = 0
        
        #start player1 moving once ball is far enough away from paddle center
        if (self.ball.y - self.player1.center_y > 70) or (self.ball.y - self.player1.center_y < -70):
            self.player1.velocity_y = self.ball.velocity_y / 1.3
        
        #update paddle position
        self.player1.move()
        
        #bounce ball off bottom or top
        if (self.ball.y < self.y) or (self.ball.top > self.top):
            self.ball.velocity_y *= -1

        if (self.ball.velocity_x > 43.0):
            self.ball.velocity_x = 42.9
        if (self.ball.velocity_x < -43.0):
            self.ball.velocity_x = -42.9
        
        #went off to a side to score point?
        if self.ball.x < self.x:
            self.player2.score += 1
            self.serve_ball(vel=self.velo)
            self.player1.center_y = self.center_y
        if self.ball.x > self.width:
            self.player1.score += 1
            self.serve_ball(vel=self.revel)
            self.player1.center_y = self.center_y
            
            
    def on_touch_move(self, touch):
        #if touch.x < self.width/3:
            #self.player1.center_y = touch.y
        if touch.x > self.width - self.width/3:
            self.player2.center_y = touch.y


Factory.register("PongBall", PongBall)
Factory.register("PongPaddle", PongPaddle)
Factory.register("PongGame", PongGame)


class PongApp(App):
    def build(self):
        game = PongGame()
        game.serve_ball()
        Clock.schedule_interval(game.update, 1.0/60.0)
        return game



if __name__ == '__main__':
    PongApp().run()