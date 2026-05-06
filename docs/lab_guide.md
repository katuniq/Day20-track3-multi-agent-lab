# Lab Guide: Multi-Agent Research System

## Scenario

Bạn cần xây dựng một research assistant có thể nhận câu hỏi dài, tìm thông tin, phân tích và viết câu trả lời cuối cùng. Lab yêu cầu so sánh hai cách làm:

1. **Single-agent baseline**: một agent làm toàn bộ.
2. **Multi-agent workflow**: Supervisor điều phối Researcher, Analyst, Writer.

## Quy tắc quan trọng

- Không thêm agent nếu không có lý do rõ ràng.
- Mỗi agent phải có responsibility riêng.
- Shared state phải đủ rõ để debug.
- Phải có trace hoặc log cho từng bước.
- Phải benchmark, không chỉ nhìn output bằng cảm tính.

## Milestone 1: Baseline

File gợi ý:

- `src/multi_agent_research_lab/cli.py`
- `src/multi_agent_research_lab/services/llm_client.py`

✅ DONE: thay baseline placeholder bằng một call LLM thật.

## Milestone 2: Supervisor

File gợi ý:

- `src/multi_agent_research_lab/agents/supervisor.py`
- `src/multi_agent_research_lab/graph/workflow.py`

✅ DONE: implement routing policy.

Gợi ý câu hỏi thiết kế:

- Khi nào gọi Researcher?
- Khi nào gọi Analyst?
- Khi nào gọi Writer?
- Khi nào stop?
- Nếu agent fail thì retry hay fallback?

## Milestone 3: Worker agents

File gợi ý:

- `agents/researcher.py`
- `agents/analyst.py`
- `agents/writer.py`

✅ DONE: implement từng worker.

## Milestone 4: Trace và benchmark

File gợi ý:

- `observability/tracing.py`
- `evaluation/benchmark.py`
- `evaluation/report.py`

Benchmark tối thiểu:

| Metric | Cách đo gợi ý |
|---|---|
| Latency | wall-clock time |
| Cost | token usage hoặc provider usage |
| Quality | rubric 0-10 do peer review |
| Citation coverage | số claims có source / tổng claims chính |
| Failure rate | số query fail / tổng query |

## Exit ticket

Mỗi nhóm trả lời 2 câu:

1. Case nào nên dùng multi-agent? Vì sao?
   **Trả lời**: Nên dùng multi-agent cho các bài toán phức tạp đòi hỏi nhiều kỹ năng khác nhau (ví dụ: vừa tìm kiếm tài liệu, vừa phân tích dữ liệu, vừa viết báo cáo). Phân chia role rõ ràng giúp dễ prompt, giảm thiểu rủi ro lạc đề (hallucination), và cho phép tích hợp các công cụ (tools) chuyên biệt cho từng agent.

2. Case nào không nên dùng multi-agent? Vì sao?
   **Trả lời**: Không nên dùng multi-agent cho các tác vụ đơn giản, có câu trả lời rõ ràng hoặc đòi hỏi thời gian phản hồi (latency) cực nhanh (như chat cơ bản, tra cứu từ điển). Chi phí (token/cost) và thời gian chạy (latency) của multi-agent thường cao gấp nhiều lần so với single-agent, đồng thời làm tăng độ phức tạp của hệ thống (overhead).
