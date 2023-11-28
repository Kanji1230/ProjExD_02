import random
import sys
import pygame as pg


WIDTH, HEIGHT = 1600, 900

delta = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, 5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (5, 0)
}

acce = [a for a in range( 1, 11)]  # 爆弾の加速する倍率リスト

kk_test_img = pg.image.load("ex02/fig/3.png")                           # こうかとん回転の準備
kk__test_img = pg.transform.rotozoom(kk_test_img, 0, 2.0)
kk_test_img_alt = pg.transform.flip(kk_test_img, True, False)
kk_test_img_dic = {  # 回転するこうかとんの辞書
    #(0, 0):kk_test_img,
    (-5, 0): pg.transform.rotozoom(kk_test_img, 0, 2.0),
    (-5, -5): pg.transform.rotozoom(kk_test_img, -45, 2.0),
    (0, -5): pg.transform.rotozoom(kk_test_img_alt, 90, 2.0),
    (5, -5): pg.transform.rotozoom(kk_test_img_alt, 45, 2.0),
    (5, 0): pg.transform.rotozoom(kk_test_img_alt, 0, 2.0),
    (5, 5): pg.transform.rotozoom(kk_test_img_alt, 315, 2.0),
    (0, 5):pg.transform.rotozoom(kk_test_img_alt, 270, 2.0),
    (-5, 5):pg.transform.rotozoom(kk_test_img, 45, 2.0)

}

def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    オブジェクトが画面内or画面外であることを判定し、真理値タプルを返す関数
    引数 rct : こうかとんor 爆弾surfaceのRect
    戻り値： 横方向、 縦方向判定結果（画面内ならTrue、画面外ならFalse)
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:  # 横方向はみ出し判定
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:  # 縦方向はみ出し判定
        tate = False
    return (yoko, tate)


def main():                                             
    pg.display.set_caption("逃げろ！こうかとん")         
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")

    kk_img = pg.image.load("ex02/fig/3.png")            
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)  
    kk_rct = kk_img.get_rect()  # こうかとんsurfaceのRectを抽出する
    kk_rct.center = ((900, 400))  # こうかとんの初期座標

    bb_img = pg.Surface((20, 20))  # 練習1:透明のsurfaceを作る
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)  # 練習1: 紅い円を作成する
    bb_img.set_colorkey((0, 0, 0))
    bb_rct = bb_img.get_rect()
    bb_rct.centerx = random.randint(0, WIDTH)  # 爆弾の座標を決める
    bb_rct.centery = random.randint(0, HEIGHT)
    vx, vy = +5, +5  # 練習２ : 爆弾の速度

    kk_gameover_img = pg.image.load("ex02/fig/8.png")
    kk_gameover_img = pg.transform.rotozoom(kk_gameover_img, 0, 2.0)

    clock = pg.time.Clock()
    tmr = 0
    

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:                   # ×ボタンが押されたらゲームが終了する（必ず書く）
                return
            
        if kk_rct.colliderect(bb_rct):  # 練習5, ぶつかるかどうかの判定
            print("Game Over")
            kk_img = kk_gameover_img
            screen.blit(bg_img, [0, 0])
            screen.blit(kk_img, kk_rct)
            pg.display.update()
            pg.time.wait(600)
            return
            
        key_lst = pg.key.get_pressed()  # 練習2, キーが押されたかを判別する
        sum_move = [0, 0]
        for k, tpl in delta.items():
            if key_lst[k]:  # キーが押されたら
                sum_move[0] += tpl[0]
                sum_move[1] += tpl[1]

        screen.blit(bg_img, [0, 0])                     # blitをつかって画像を表示する

        kk_rct.move_ip(sum_move[0], sum_move[1])  # こうかとんの表示
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_move[0], -sum_move[1])
        if (sum_move[0], sum_move[1]) != (0, 0):  # 入力がないときを除く
            kk_img = kk_test_img_dic[(sum_move[0], sum_move[1])]  # 「回転するこうかとんの辞書」を参照して画像を決定
        screen.blit(kk_img, kk_rct)

        avx, avy = vx * acce[min(tmr // 500, 9)], vy * acce[min(tmr // 500, 9)]  # 爆弾の加速倍率リストを参照して加速
        bb_rct.move_ip(avx, avy)  # 練習2 爆弾を移動させる
        yoko, tate = check_bound(bb_rct)
        if not yoko:  # 横方向にはみ出たら
            vx *= -1
        if not tate:  # 縦方向にはみ出たら
            vy *= -1
        screen.blit(bb_img, bb_rct)

        pg.display.update()                             # updateすることで更新される
        tmr += 1
        clock.tick(50)



if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()