# Design Template

## Problem

Hệ thống cần xử lý các câu hỏi nghiên cứu phức tạp đòi hỏi thu thập thông tin từ nhiều nguồn, phân tích các góc nhìn khác nhau, và tổng hợp thành một báo cáo hoàn chỉnh, có trích dẫn rõ ràng.

## Why multi-agent?

Single-agent gặp khó khăn khi phải vừa tìm kiếm, vừa trích xuất thông tin, và vừa tổng hợp cùng lúc. Cách tiếp cận multi-agent giúp chia nhỏ luồng công việc (phân công theo role: tìm kiếm, phân tích, viết bài, và kiểm tra chéo) để mỗi agent tập trung hoàn thành một nhiệm vụ cụ thể, từ đó nâng cao chất lượng đầu ra.

## Agent roles

| Agent | Responsibility | Input | Output | Failure mode |
|---|---|---|---|---|
| Supervisor | Điều phối luồng công việc | Trạng thái hiện tại (ResearchState) | Chuyển trạng thái sang agent tiếp theo | Vòng lặp vô hạn nếu không kiểm tra số lần lặp |
| Researcher | Tìm kiếm thông tin & ghi chú | Truy vấn người dùng | Ghi chú nghiên cứu (research_notes) | Lỗi từ API tìm kiếm |
| Analyst | Phân tích và cấu trúc lại thông tin | Ghi chú nghiên cứu | Ghi chú phân tích (analysis_notes) | Thông tin không đủ sâu |
| Writer | Viết bài tổng hợp | Ghi chú nghiên cứu và phân tích | Câu trả lời cuối cùng (final_answer) | Lạc đề hoặc bỏ sót trích dẫn |
| Critic | Kiểm tra thông tin (hallucination) | Câu trả lời cuối cùng | Nhận xét (critique) | Đánh giá sai |

## Shared state

- `request`: Câu hỏi gốc của người dùng.
- `research_notes`: Ghi chú từ Researcher, giúp Analyst và Writer có thông tin nền tảng.
- `analysis_notes`: Ghi chú từ Analyst, giúp Writer có góc nhìn sâu hơn.
- `final_answer`: Kết quả cuối cùng.
- `route_history`: Lịch sử các bước đã qua, giúp Supervisor quyết định bước tiếp theo.
- `iteration`: Số vòng lặp để chặn vòng lặp vô hạn.

## Routing policy

Luồng chạy tuyến tính (Linear Pipeline):
`Supervisor -> Researcher -> Supervisor -> Analyst -> Supervisor -> Writer -> Critic -> Supervisor -> END`
- Supervisor quyết định bước tiếp dựa vào `route_history`.
- Giới hạn tối đa 5 vòng lặp, nếu quá sẽ force `done`.

## Guardrails

- Max iterations: 5
- Timeout: 60s
- Retry: Có (handled by underlying LangChain/OpenAI SDK cho rate limit).
- Fallback: Trả về Mock search results nếu thiếu Tavily API key.
- Validation: Pydantic schemas giúp validate input/output giữa các bước.

## Benchmark plan

- Câu hỏi test: "Research GraphRAG state-of-the-art and write a 500-word summary"
- Metrics: Latency (giây), Quality (1-10), và Cost (USD).
- Expected outcome: Mô hình multi-agent chạy chậm hơn và tốn phí hơn chút ít, nhưng chất lượng vượt trội (điểm 9/10), có bằng chứng và dẫn chứng đầy đủ hơn so với Single-agent baseline.
