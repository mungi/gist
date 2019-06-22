# tmux 단축키 & 치트시트

실행하기:

    tmux

세션명을 주면서 시작하기:

    tmux new -s myname

붙이기:

    tmux a  #  (또는 at이나 attach)

특정 세션에 붙이기:

    tmux a -t myname

세션 일람:

    tmux ls

세션 강제종료:

    tmux kill-session -t myname

tmux 내에서 Prefix 인 'Ctrl-b'를 누르고

## 세션

    :new<CR>  새로운 세션
    s  세션 리스트
    $  세션에 이름 정하기

## 윈도우 (탭)

    c  새 윈도우
    w  윈도우 리스
    f  윈도우 찾기
    ,  윈도우에 이름 붙이기
    &  윈도우 강제 닫기

## 패널 (화면 구분)

    %  세로로 나누기
    "  가로로 나누기
    
    o  패널 바꾸기
    q  패널 번호 보여주기
    x  패널 강제종료
    +  패널을 새 윈도우로 이동 (마우스로 드래그해서 선택하기 위해서 라든지)
    -  윈도우에서 패널로 복귀
    ⍽  스페이스 - 레이아웃을 토글
    {  패널을 욎쪽으로 이동
    }  패널을 오른쪽으로 이동
    
    z Zoom 기능, 패널을 윈도 하나로 확대한다. 다시 'Prefix'-z 하면 해당 패널로 원복 된다.

## 패널 크기 조절하기
    Prifix Key를 누르고 Ctrl를 누른 채로 방향키로 크기조절 가능

레이아웃이 자동으로 정해주는 크기가 마음에 안들 때 패널크기를 조절하기위해서 사용합니다. 제 개인적으로는 거의 안씁니다만 알아두면 편리합니다. 여기 패널크기를 조절하는 기본적인 키들입니다.

    : resize-pane --- 아래쪽로 조절 (저는 -D가 아래로. 원문에는 아무것도 적지 않으면 아래로 라고 하네요)
    : resize-pane -U --- 위쪽로 조절
    : resize-pane -L --- 왼쪽으로 조절
    : resize-pane -R --- 오른쪽으로 조절
    : resize-pane 20 --- 아래로 20칸 조절 (저는 -D가 아래로. 원문에는 아무것도 적지 않으면 아래로 라고 하네요. )
    : resize-pane -U 20 --- 위로 20칸 조절
    : resize-pane -L 20 --- 왼쪽으로 20칸 조절
    : resize-pane -R 20 --- 오른쪽으로 20칸 조절
    : resize-pane -t 2 20 --- 2번 패널 아래로 20칸 조절 (저는 -D가 아래로. )
    : resize-pane -t 2 -L 20 --- 2번 패널 왼쪽으로 20칸 조절

## 카피 모드:

Prefix(Ctrl-b)를 누르고 [ 를 누르면 카피모드가 됩니다. 그러면 커서키를 이용해서 화면을 이리저리 다니는 것이 가능합니다. 기본적으로 방향키로 지정되어 있습니다만 설정 파일을 이용해서 vim키로 변경을하면 윈도우나 패널 사이를 이동하기 위해서 손의 위치를 움직일 필요가 없어집니다.tmux 버퍼를 조작하기 위한 vi모드가 있습니다. 활성화 시키려면 아래의 라인을 .tmux.conf에 기술합니다.

    setw -g mode-keys vi

이렇게 하면 h, j, k, l을 이용해서 버퍼에서 이동을 할 수 있게 됩니다.

카피모드에서 나오려면 엔터를 누르면 됩니다. 한 글자 단위로 이동하는 것은 별로 효율적이지 않습니다.vi 모드를 활성화했기 때문에 여러가지 편리한 키들도 활성화 되어 있습니다.
예를 들면 "w" 키를 이용해서 다음 단어로 이동한다거나 "b"를 누르면 앞의 단어로 이동합니다. "f"키를 사용해서 그 줄의 어떤 문자의 의치로 점프할 수도 있고 "F"를 이용해서 그 줄의 앞 방향으로 어떤 문자의 위치로 점프할 수 있습니다.

       기능                     vi             emacs
       Back to indentation     ^              M-m
       Clear selection         Escape         C-g
       Copy selection          Enter          M-w
       Cursor down             j              Down
       Cursor left             h              Left
       Cursor right            l              Right
       Cursor to bottom line   L
       Cursor to middle line   M              M-r
       Cursor to top line      H              M-R
       Cursor up               k              Up
       Delete entire line      d              C-u
       Delete to end of line   D              C-k
       End of line             $              C-e
       Goto line               :              g
       Half page down          C-d            M-Down
       Half page up            C-u            M-Up
       Next page               C-f            Page down
       Next word               w              M-f
       Paste buffer            p              C-y
       Previous page           C-b            Page up
       Previous word           b              M-b
       Quit mode               q              Escape
       Scroll down             C-Down or J    C-Down
       Scroll up               C-Up or K      C-Up
       Search again            n              n
       Search backward         ?              C-r
       Search forward          /              C-s
       Start of line           0              C-a
       Start selection         Space          C-Space
       Transpose chars                        C-t

## 기타

    d  세션과 터미널 분리 detach
    t  전체화면 시계
    ?  단축키 일람
    :  프롬프트

## 설정 옵션
    # Prefix 변경 Ctrl-b 에서  Ctrl-a로 바꿀려면 아래 3줄 주석 해제
    #unbind C-b
    #set-option -g prefix C-a
    #bind-key C-a send-prefix

    # 터미널 모드를 256컬러
    set -g default-terminal "screen-256color"

    # UTF-8 설정 (Powerline 깨질 때)
    setw -gq utf8 on
    
    # 활동 알림 활성화
    setw -g monitor-activity on
    set -g visual-activity on

    # 마우스 사용 On 단축키 지정 : ^B m
    bind m \
      set -g mode-mouse on \;\
      set -g mouse-resize-pane on \;\
      set -g mouse-select-pane on \;\
      set -g mouse-select-window on \;\
      display 'Mouse: ON'

    # 마우스 사용 Off 단축키 지정 : ^B M
    bind M \
      set -g mode-mouse off \;\
      set -g mouse-resize-pane off \;\
      set -g mouse-select-pane off \;\
      set -g mouse-select-window off \;\
      display 'Mouse: OFF'

## 참조
- https://www.hamvocke.com/blog/a-guide-to-customizing-your-tmux-conf/
