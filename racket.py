from kivy.clock import Clock
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.uix.widget import Widget

from configurables import racketMoveAmount, racketClickAccuracyTop, racketClickAccuracyBottom, \
    bigBrickRacketFitAccuracy, racketY, racketWaitTime, racketMoveTime, racketMoveTransition


class Racket(Widget):
    def __init__(self, *args, **kwargs):
        super(Racket, self).__init__(*args, **kwargs)

        self.canMove = True

        Window.bind(on_key_down=self.key_down)

        self.doesBrickFitCallback = True
        self.bigBrick = None

    def key_down(self, _, keycode, _2, _3, _4):
        if not self.canMove: return

        elif keycode == 274:
            if len(self.bigBrick.brickQueue) != 0 and "y" in self.bigBrick.pos_hint:
                self.swipe_down(*self.bigBrick.get_queue_and_ys())


    def on_touch_down(self, touch):
        if not self.canMove: return

        if self.y - (self.parent.height * racketClickAccuracyBottom) <= touch.y \
                <= self.top + (self.parent.height * racketClickAccuracyTop):
            self.center_x = touch.x

    def on_touch_move(self, touch):
        if not self.canMove: return

        if self.y - (self.parent.height * racketClickAccuracyBottom) <= touch.y \
                <= self.top + (self.parent.height * racketClickAccuracyTop):
            self.center_x = touch.x

    def swipe_down(self, x, hitY, missY):
        self.canMove = False

        bbrfa = bigBrickRacketFitAccuracy * self.parent.width

        del self.pos_hint["y"]

        if (x - bbrfa) <= self.x <= (x + bbrfa):
            self.x = x

            a = Animation(y=hitY, duration=racketMoveTime, transition=racketMoveTransition)
            a.bind(on_complete=lambda _=None, _2=None: self.swiped(True))
            a.start(self)

        else:
            a = Animation(y=missY, duration=racketMoveTime, transition=racketMoveTransition)
            a.bind(on_complete=lambda _=None, _2=None: self.swiped(False))
            a.start(self)

    def swiped(self, hit):
        self.doesBrickFitCallback(hit)


        a = Animation(y=self.parent.height * racketY, duration=racketMoveTime, transition=racketMoveTransition)
        a.bind(on_complete=self.movement_done)
        Clock.schedule_once(lambda _: a.start(self), racketWaitTime)

    def movement_done(self, _=None, _2=None):
        self.canMove = True

        self.pos_hint["y"] = racketY

    def reset(self):
        self.center_x = self.parent.width / 2
