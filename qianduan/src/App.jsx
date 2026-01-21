import React, { useState, useRef, useEffect } from "react";

// API 配置 - 后端 FastAPI 接口地址
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

export const App = () => {
  const [messages, setMessages] = useState([
    {
      role: "assistant",
      content: "你好！我是你的故事助手，告诉我你想要什么样的故事，我会帮你编织出来。"
    }
  ]);
  const [inputValue, setInputValue] = useState("");
  const [loading, setLoading] = useState(false);
  const [showDialog, setShowDialog] = useState(true);
  // 漫画图片数组，初始为默认的静态图片
  const [comicImages, setComicImages] = useState(
    Array.from({ length: 9 }, (_, index) => `/resource/IMG_${index + 1}.jpg`)
  );
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  // 自动滚动到底部
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // 调用后端 API
  const sendMessage = async () => {
    if (!inputValue.trim() || loading) return;

    const userMessage = {
      role: "user",
      content: inputValue.trim()
    };

    // 添加用户消息
    setMessages((prev) => [...prev, userMessage]);
    setInputValue("");
    setLoading(true);

    try {
      const response = await fetch(`${API_BASE_URL}/api/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          messages: [...messages, userMessage]
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      
      // 判断是否包含漫画图片：只有当返回明确包含9张图片时才更新展示区
      const hasComicImages = data.images && 
                            Array.isArray(data.images) && 
                            data.images.length === 9;
      
      if (hasComicImages) {
        // 有漫画时：更新右侧漫画展示区域的图片
        setComicImages(data.images);
      }
      // 没有漫画时：不做任何操作，保持展示区原有图片不变
      
      // 构建助手回复内容：包含文字信息和漫画信息
      let assistantContent = data.response || data.message || "抱歉，我暂时无法回复。";
      
      // 只有当有漫画时才添加漫画相关的提示信息
      if (hasComicImages) {
        if (data.comic_info) {
          assistantContent += `\n\n📖 漫画信息：${data.comic_info}`;
        } else {
          assistantContent += `\n\n✨ 已生成 9 张漫画图片，请查看右侧展示区。`;
        }
      }
      
      // 添加助手回复
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: assistantContent
        }
      ]);
    } catch (error) {
      console.error("Error calling API:", error);
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: "抱歉，连接服务器时出现了问题，请稍后再试。"
        }
      ]);
    } finally {
      setLoading(false);
      inputRef.current?.focus();
    }
  };

  // 处理回车发送
  const handleKeyPress = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  // 清空对话
  const clearMessages = () => {
    setMessages([
      {
        role: "assistant",
        content: "对话已清空，让我们重新开始吧！"
      }
    ]);
    // 重置为默认图片
    setComicImages(
      Array.from({ length: 9 }, (_, index) => `/resource/IMG_${index + 1}.jpg`)
    );
  };

  return (
    <div className="page">
      <div className="storybook-shell">
        <header className="page-header">
          <div>
            <div className="page-title">storybook</div>
            <div className="page-subtitle">
              根据对话，编织出你想要的故事。
            </div>
          </div>
        </header>

        <div className="storybook-header">
          <div className="badge">Storybook Demo</div>
          <button
            className="ghost-button"
            onClick={() => setShowDialog((v) => !v)}
          >
            {showDialog ? "收起展示区" : "展开展示区"}
          </button>
        </div>

        <div className="storybook-layout">
          {/* 左侧：交互对话框 */}
          <section className="storybook-panel storybook-panel--chat">
            <div className="chat-header">
              <h2 className="dialog-title">对话</h2>
              <button
                className="ghost-button ghost-button--small"
                onClick={clearMessages}
                title="清空对话"
              >
                清空
              </button>
            </div>

            <div className="chat-messages">
              {messages.map((msg, index) => (
                <div
                  key={index}
                  className={`bubble bubble--${msg.role === "user" ? "user" : "system"}`}
                >
                  <p>{msg.content}</p>
                </div>
              ))}
              {loading && (
                <div className="bubble bubble--system">
                  <p className="loading-text">正在思考...</p>
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>

            <div className="chat-input-container">
              <textarea
                ref={inputRef}
                className="chat-input"
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="输入你的想法，按 Enter 发送..."
                rows={2}
                disabled={loading}
              />
              <button
                className="chat-send-button"
                onClick={sendMessage}
                disabled={!inputValue.trim() || loading}
              >
                发送
              </button>
            </div>
          </section>

          {/* 右侧：漫画展示区 */}
          {showDialog && (
            <section className="storybook-panel storybook-panel--dialog">
              <h2 className="dialog-title">漫画展示</h2>

              <div className="display-grid display-grid--nine">
                {comicImages.map((imageSrc, index) => (
                  <div key={index} className="display-card display-card--comic">
                    <img
                      src={imageSrc}
                      alt={`分镜 ${index + 1}`}
                      className="display-card-image"
                      onError={(e) => {
                        // 如果图片加载失败，显示默认图片
                        e.target.src = `/resource/IMG_${index + 1}.jpg`;
                      }}
                    />
                  </div>
                ))}
              </div>
            </section>
          )}
        </div>
      </div>
    </div>
  );
};

