import React, { useState } from "react";

const scenes = [
  {
    id: "intro",
    title: "黄昏下的故事书",
    text: "黄昏的光洒在米黄色的书页上，你翻开了这本久违的故事书，淡淡的纸张香味扑面而来。",
    options: [
      {
        label: "轻轻翻到下一页",
        next: "garden"
      },
      {
        label: "合上书本，先观察一下四周",
        next: "room"
      }
    ]
  },
  {
    id: "garden",
    title: "花园的低语",
    text: "书页上的画面渐渐活了起来，你仿佛被带到一座安静的花园，暖黄色的灯光点缀其间。",
    options: [
      {
        label: "沿着石板路走进去",
        next: "path"
      },
      {
        label: "坐在长椅上静静发呆",
        next: "bench"
      }
    ]
  },
  {
    id: "room",
    title: "安静的房间",
    text: "房间里只有柔和的台灯亮着，米黄色的墙壁让一切显得格外温柔。",
    options: [
      {
        label: "重新打开故事书",
        next: "intro"
      }
    ]
  },
  {
    id: "path",
    title: "分岔的小路",
    text: "前方出现了一处分岔口，左边是被灯光染成蜂蜜色的小径，右边是被树影覆盖的静谧小道。",
    options: [
      {
        label: "走向蜂蜜色的小径",
        next: "lightPath"
      },
      {
        label: "走向静谧的小道",
        next: "quietPath"
      }
    ]
  },
  {
    id: "bench",
    title: "短暂的停留",
    text: "你坐在木质长椅上，感受着微风拂过纸页，故事似乎在等待你的下一个决定。",
    options: [
      {
        label: "继续阅读故事",
        next: "garden"
      },
      {
        label: "回到现实世界",
        next: "end"
      }
    ]
  },
  {
    id: "lightPath",
    title: "温暖的尽头",
    text: "小径尽头是一扇半掩的木门，门后透出柔和的米黄色灯光，让人忍不住想推门而入。",
    options: [
      {
        label: "推开木门",
        next: "endWarm"
      },
      {
        label: "返回花园入口",
        next: "garden"
      }
    ]
  },
  {
    id: "quietPath",
    title: "安静的秘密",
    text: "树影之间，你看到一本和手中一模一样的故事书正静静地放在石头上，仿佛在等你拿起。",
    options: [
      {
        label: "拿起那本故事书",
        next: "mirror"
      },
      {
        label: "慢慢退回原路",
        next: "garden"
      }
    ]
  },
  {
    id: "mirror",
    title: "故事中的故事",
    text: "当你翻开那本故事书，第一页写着你的名字，而故事，正从你现在所做的选择开始。",
    options: [
      {
        label: "合上书本，回到最初的页面",
        next: "intro"
      },
      {
        label: "在这里停下，把故事留给未来的自己",
        next: "end"
      }
    ]
  },
  {
    id: "endWarm",
    title: "柔光里的结尾",
    text: "门后是一间温暖的房间，墙上挂着你走过的每一个场景。你意识到，真正的故事一直都在你心里。",
    options: [
      {
        label: "回到故事开头，再读一遍",
        next: "intro"
      },
      {
        label: "带着这份温暖离开",
        next: "end"
      }
    ]
  },
  {
    id: "end",
    title: "故事暂时合上",
    text: "你轻轻合上故事书，米黄色的封面在灯光下安静地躺着。这不是结束，只是一次温柔的暂停。",
    options: [
      {
        label: "重新开始故事",
        next: "intro"
      }
    ]
  }
];

const findScene = (id) => scenes.find((s) => s.id === id) || scenes[0];

export const App = () => {
  const [currentId, setCurrentId] = useState("intro");
  const [showDialog, setShowDialog] = useState(true);

  const scene = findScene(currentId);

  return (
    <div className="page">
      <div className="storybook-shell">
        <div className="storybook-header">
          <div className="badge">Storybook Demo</div>
          <button
            className="ghost-button"
            onClick={() => setShowDialog((v) => !v)}
          >
            {showDialog ? "收起对话框" : "展开对话框"}
          </button>
        </div>

        <div className="storybook-layout">
          <section className="storybook-panel storybook-panel--story">
            <h1 className="storybook-title">{scene.title}</h1>
            <p className="storybook-text">{scene.text}</p>

            <div className="choice-list">
              {scene.options.map((opt) => (
                <button
                  key={opt.label}
                  className="choice-button"
                  onClick={() => setCurrentId(opt.next)}
                >
                  {opt.label}
                </button>
              ))}
            </div>
          </section>

          {showDialog && (
            <section className="storybook-panel storybook-panel--dialog">
              <h2 className="dialog-title">对话框</h2>
              <p className="dialog-tip">
                这里模拟的是「旁白 / 系统」与「读者」之间的互动。
              </p>

              <div className="dialog-bubbles">
                <div className="bubble bubble--system">
                  <span className="bubble-label">旁白</span>
                  <p>你现在停留在「{scene.title}」，想好了下一步要去哪里了吗？</p>
                </div>

                <div className="bubble bubble--user">
                  <span className="bubble-label">你</span>
                  <p>
                    {scene.options.length > 1
                      ? "让我再看看选项，我想做一个不一样的选择。"
                      : "我已经知道答案了，准备重新开始。"}
                  </p>
                </div>
              </div>

              <div className="dialog-footer">
                <button
                  className="ghost-button ghost-button--small"
                  onClick={() => setCurrentId("intro")}
                >
                  回到开篇
                </button>
                <span className="dialog-hint">你可以随时点击左侧的选项改变故事走向。</span>
              </div>
            </section>
          )}
        </div>
      </div>
    </div>
  );
};

