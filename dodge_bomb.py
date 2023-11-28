import sys
import pygame as pg


WIDTH, HEIGHT = 1600, 900


def main():                                             #メイン関数
    pg.display.set_caption("逃げろ！こうかとん")         #ウィンドウの名前を「逃げろ！こうかんとん」にしている
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")
    kk_img = pg.image.load("ex02/fig/3.png")            #サーフェイスというクラスになっている
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)      #拡大縮小
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:                   #×ボタンが押されたらゲームが終了する（必ず書く）
                return

        screen.blit(bg_img, [0, 0])                     #blitをつかって画像を表示する
        screen.blit(kk_img, [900, 400])
        pg.display.update()                             #updateすることで更新される
        tmr += 1
        clock.tick(10)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()