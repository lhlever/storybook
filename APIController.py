from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import uvicorn
from starlette.middleware.cors import CORSMiddleware

from agent_core import StoryCreationAgent
from memory import MemorySystem


# 引入我们在上面定义的业务逻辑模块
# from LLM_conversion import generate_story_data


# ================= Pydantic 模型定义 (用于Swagger文档和校验) =================
class StoryRequest(BaseModel):
    prompt: str = Field(..., example="给我创作一个一家五口三代同堂，在一个200平米的大平层房子里温馨的一天")


class StoryboardFrame(BaseModel):
    frame_index: int
    scene_description: str
    visual_prompt: str


class StoryResponse(BaseModel):
    main_story: str
    character_settings: str
    frames: List[StoryboardFrame]


# ================= FastAPI 实例 =================
app = FastAPI(title="Storybook Generator API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 开发环境临时使用
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/generate_storybook")
async def api_generate_storybook(request: StoryRequest):
    """
    API 入口：接收前端请求 -> 调用业务逻辑 -> 返回结果
    """
    print(f"收到生成请求: {request.prompt}")

    try:
        # 调用分离出去的业务逻辑函数
        # data = generate_story_data(request.prompt)
        comic_idea = request.prompt
        print("=" * 70)
        print("🎨 测试漫画生成 Agent")
        print("=" * 70)
        print(f"\n📝 漫画创意: {comic_idea}")
        print("\n" + "-" * 70)

        # 创建项目
        project_name = "测试漫画"

        # 初始化 Memory
        memory = MemorySystem(project_name)
        memory.profile.update_settings({
            "project_type": "comic",
            "comic_style": "manga"
        })

        # 创建 Agent
        agent = StoryCreationAgent(memory)

        # 运行流程
        print("\n🚀 开始运行 Agent...\n")
        result = agent.run(project_name, comic_idea)

        # 输出结果
        print("\n" + "=" * 70)
        print("✅ 运行完成！以下是生成结果：")
        print("=" * 70)

        print(f"\n📊 生成了 {len(result)} 格漫画\n")

        # 显示每一格的内容
        for i, item in enumerate(result, 1):
            word = item.get("word", "无文本")
            url = item.get("url", "无URL")

            print(f"【第 {i} 格】")
            print(f"  文本: {word}")
            print(f"  图片: {url}")
            print()

        # 保存结果到 JSON 文件
        import json
        output_file = f"output/{project_name}_result.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        print(f"💾 结果已保存到: {output_file}")

        print("\n" + "=" * 70)
        print("🎉 测试完成！")
        print("=" * 70)
        return result

        # # 数据完整性兜底处理
        # frames = data.get("frames", [])
        # # 确保只取前9帧（虽然Prompt要求了9帧，但做个防御性编程）
        # if len(frames) > 9:
        #     frames = frames[:9]

        # return StoryResponse(
        #     main_story=data.get("main_story", "生成失败，未获取到故事内容"),
        #     character_settings=data.get("character_settings", "无设定"),
        #     frames=[
        #         StoryboardFrame(
        #             frame_index=f.get("frame_index", i + 1),
        #             scene_description=f.get("scene_description", ""),
        #             visual_prompt=f.get("visual_prompt", "")
        #         ) for i, f in enumerate(frames)
        #     ]
        # )

    except Exception as e:
        # 捕获 service 层抛出的异常，转化为 HTTP 500
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)