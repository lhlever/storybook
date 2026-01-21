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
  // 存储格式：每个元素为 { src: 图片地址, word: 文字描述 | null }
  const [comicImages, setComicImages] = useState(
    Array.from({ length: 9 }, (_, index) => ({
      src: `/resource/IMG_${index + 1}.jpg`,
      word: null
    }))
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
    const userInputContent = inputValue.trim(); // 保存用户输入的内容
    setInputValue("");
    setLoading(true);

    try {
      // 直接调用接口，发送的内容就是用户刚刚输入的那句话
      const response = await fetch("http://10.35.68.63:8000/api/generate_storybook", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          prompt: userInputContent
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      // 后端当前返回的数据结构就是一个数组：
      // [
      //   { word: '...', url: { url: '图片地址', ... } },
      //   ...
      // ]
      const imagesData = Array.isArray(data) ? data : [];
      
      // 判断是否包含漫画图片数据：至少有 1 条，并且每组数据包含 word 和 url.url
      const hasComicImages =
        Array.isArray(imagesData) &&
        imagesData.length > 0 &&
        imagesData.every((item) => item.word && item.url && item.url.url);
      
      if (hasComicImages) {
        // 有漫画时：直接使用后端返回的图片地址和文字，不再进行Canvas合成
        // 如果返回的数量不是 9 条，也照样展示（展示返回的所有分镜）
        const imagesWithWord = imagesData.map((item, index) => ({
          src:
            (item.url && typeof item.url === "string" && item.url) ||
            (item.url && typeof item.url === "object" && item.url.url) ||
            `/resource/IMG_${index + 1}.jpg`,
          word: item.word || null
        }));
        setComicImages(imagesWithWord);
      }
      // 没有漫画时：不做任何操作，保持展示区原有图片不变
      
      // 构建助手回复内容：如果有漫画，显示"故事已生成"
      let assistantContent = "";
      if (hasComicImages) {
        assistantContent = "故事已生成";
      } else {
        // 没有漫画时，尝试显示接口返回的文本信息；否则给出默认提示
        const baseReply =
          !Array.isArray(data) && typeof data === "object"
            ? data.response || data.message
            : null;
        assistantContent = baseReply || "抱歉，这次没有生成故事。";
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
      Array.from({ length: 9 }, (_, index) => ({
        src: `/resource/IMG_${index + 1}.jpg`,
        word: null
      }))
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
                {comicImages.map((item, index) => (
                  <div key={index} className="display-card display-card--comic">
                    {item.word && (
                      <div className="display-card-word">
                        {item.word}
                      </div>
                    )}
                    <img
                      src={item.src}
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

