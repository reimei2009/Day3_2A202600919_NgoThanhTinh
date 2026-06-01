# Báo Cáo Cá Nhân - Travel Assistant Project

## Giới Thiệu

Em tên là Ngô Thanh Tình. Trong bài tập này, em đã đóng góp vào việc xây dựng Travel Assistant với 2 loại agent: Chatbot Baseline và ReAct Agent. Báo cáo này sẽ chia sẻ trải nghiệm, những gì em đã học được và những thử thách em đã vượt qua.

## Vai Trò Của Trong Nhóm

Trong project này, em chủ yếu tập trung vào các phần sau:

### 1. API Configuration & Testing
Đây là phần đầu tiên và cũng là phần khó nhất em làm.

**Những gì đã làm:**
- Test nhiều API providers khác nhau (OpenAI, Z.AI, MIMO)
- Debug endpoint URLs (sửa lỗi thiếu trailing slash)
- Kiểm tra model availability
- Config MIMO API thành công

**Khó khăn gặp phải:**
- OpenAI API bị quota exceeded - không thể dùng
- Z.AI model names không đúng - báo lỗi "Param Incorrect"
- Endpoint URL bị sai 404 errors

**Cách giải quyết:**
- Research documentations của từng API
- Test từng model một cách hệ thống
- Thử nhiều endpoint URLs khác nhau
- Cuối cùng tìm được MIMO API với 75B tokens quota

### 2. ReAct Agent Implementation
Em đã giúp implement ReAct pattern cho travel agent.

**Những gì đã làm:**
- Design system prompt cho ReAct agent
- Implement Thought-Action-Observation loop
- Integrate 7 travel tools
- Handle parsing và tool execution

**Khó khăn gặp phải:**
- LLM không luôn parse action đúng format
- Tool parameters extraction phức tạp
- Error handling khi tools fail

**Cách giải quyết:**
- Sử dụng regex để parse action strings
- Implement flexible parameter matching
- Add try-catch blocks với meaningful error messages

### 3. UI/UX Development
cải thiện giao diện Streamlit.

**Những gì em đã làm:**
- Thêm custom CSS cho modern design
- Implement pending state với typing indicator
- Auto-clear input functionality
- Enter key support

**Khó khăn gặp phải:**
- Streamlit styling limitations
- Input clearing timing issues
- Pending state implementation

**Cách giải quyết:**
- Use inline CSS with gradients và shadows
- Implement 2-step process (add pending → replace with response)
- Use st.chat_input() thay vì st.form()

### 4. Testing & Debugging
Em đã thực hiện extensive testing.

**Những gì em đã làm:**
- Test tất cả 7 tools
- Test với 5 different queries
- Debug rate limiting issues
- Generate test reports

**Khó khăn gặp phải:**
- Rate limiting (429 errors)
- Token usage tracking
- Performance optimization

**Cách giải quyết:**
- Add delay giữa requests
- Use 2 API keys alternately
- Implement retry logic

## Những Kiến Thức Em Học Được

### Technical Skills

#### 1. ReAct Pattern
Trước project này, em chỉ biết LLM là "input → output". Nhưng sau khi làm ReAct agent, em hiểu rằng:

**ReAct = Reasoning + Acting**
- **Reasoning**: LLM suy nghĩ về vấn đề
- **Acting**: LLM quyết định action cụ thể
- **Observation**: Nhận feedback từ environment
- **Lặp lại**: Cho đến khi có solution

Điều này giúp LLM không chỉ trả lời question mà còn có thể **thực hiện task**.

#### 2. Tool Integration
Em học được cách integrate external tools với LLM:

**Challenges:**
- Parse tool parameters từ LLM response
- Handle tool failures gracefully
- Format tool outputs để LLM hiểu

**Lessons learned:**
- Regex là bạn thân trong parsing
- Error handling là super important
- Tool output format phải consistent

#### 3. API Management
Em đã học rất nhiều về working với APIs:

**Challenges:**
- Multiple API providers with different formats
- Rate limiting và quota management
- Authentication và error handling

**Lessons learned:**
- Always read documentation carefully
- Test with simple queries first
- Implement retry logic
- Use multiple API keys for backup

#### 4. UI/UX Design
Streamlit là framework mới với em, nhưng em đã học được:

**Challenges:**
- Custom styling limitations
- State management
- User experience optimization

**Lessons learned:**
- Inline CSS works wonders
- Pending states improve UX significantly
- Auto-clear input makes experience smoother

### Soft Skills

#### 1. Problem Solving
Project này đã test em về problem solving skills:

**Examples:**
- API configuration: Test 3 different APIs trước khi tìm được working one
- Tool integration: Debug parameter extraction issues
- Rate limiting: Add delays và retry logic

**Key insight:** Problem solving là về **persistence** và **systematic approach**.

#### 2. Research Skills
Em đã học cách research efficiently:

**Examples:**
- Read API documentations
- Search for similar issues online
- Test hypotheses systematically

**Key insight:** Good research saves time in long run.

#### 3. Time Management
Em học được cách balance giữa features và deadlines:

**Examples:**
- Prioritize core functionality first (ReAct agent)
- Then add enhancements (UI improvements)
- Test thoroughly before moving on

**Key insight:** Done is better than perfect, but quality matters.

## Những Thử Thách Đã Vượt Qua

### Challenge 1: API Configuration Hell
**Problem:** OpenAI quota exceeded, Z.AI model names wrong, endpoint 404 errors

**Process:**
1. Test OpenAI → quota exceeded ❌
2. Test Z.AI → model names wrong ❌
3. Research MIMO API → find working endpoint ✅
4. Test all models → only mimo-v2.5-pro works ✅

**Learning:** Systematic testing pays off.

### Challenge 2: Tool Integration Complexity
**Problem:** LLM not parsing actions correctly

**Process:**
1. Analyze LLM responses → inconsistent formats
2. Improve system prompt → better but not perfect
3. Add regex parsing → handles edge cases
4. Add error handling → graceful failures

**Learning:** Flexibility is key when working with LLMs.

### Challenge 3: Rate Limiting Frustration
**Problem:** Getting 429 errors frequently

**Process:**
1. Add delay between requests → helps but not enough
2. Implement retry logic → better
3. Use 2 API keys alternately → solves it

**Learning:** Always have backup plans.

### Challenge 4: UI Timing Issues
**Problem:** Input clearing too early or too late

**Process:**
1. Use st.form() with clear_on_submit → clears too early
2. Try manual clearing → too complex
3. Use st.chat_input() → perfect timing
4. Add pending state → even better UX

**Learning:** UX requires thinking through user journey.

## Những điểm hài lòng

1. ✅ **API Configuration Success**
   - Em đã test 3 different APIs
   - Found working solution (MIMO)
   - Learned valuable lessons about API management

2. ✅ **ReAct Agent Implementation**
   - Em helped implement Thought-Action-Observation loop
   - Integrated 7 tools successfully
   - All test cases pass

3. ✅ **UI/UX Improvements**
   - Added modern design with CSS
   - Implemented pending state
   - Auto-clear input functionality

4. ✅ **Problem Solving**
   - Overcame API challenges
   - Fixed tool integration issues
   - Handled rate limiting

## Những Điểm Cần Cải Thiện

1. ❌ **Testing More Thoroughly**
   - Should test more edge cases
   - Need better test coverage
   - Should implement unit tests

2. ❌ **Documentation**
   - Could document code better
   - Should add more comments
   - Need better README

3. ❌ **Performance Optimization**
   - Token usage could be lower
   - Response time could be faster
   - Caching could be implemented

## Kế Hoạch Phát Triển Cá Nhân

### Short-term (1-3 months)
1. **Deepen ReAct Knowledge**
   - Research advanced ReAct patterns
   - Study LangChain implementation
   - Experiment with more complex tools

2. **Improve API Skills**
   - Learn more about rate limiting strategies
   - Study API design patterns
   - Practice with more APIs

3. **Enhance UI/UX Skills**
   - Learn more CSS/JavaScript
   - Study modern UI patterns
   - Practice with more frameworks

### Long-term (6-12 months)
1. **Advanced LLM Applications**
   - Study multi-agent systems
   - Learn about agent orchestration
   - Experiment with autonomous agents

2. **Production Deployment**
   - Learn Docker and containerization
   - Study cloud deployment
   - Learn about monitoring and scaling

3. **Specialization**
   - Decide whether to focus on:
     - LLM application development
     - API integration
     - UI/UX design
     - Or combination of all

## Tóm Tắt

Project này là một **experience thật sự valuable** cho em. Không chỉ học về ReAct pattern và LLM agents, mà còn học về:

- **Technical skills**: API management, tool integration, UI/UX
- **Problem solving**: Debugging, research, systematic approach
- **Soft skills**: Time management, persistence, flexibility

### Key Takeaways:

1. **ReAct Pattern is Powerful**
   - Enables LLMs to perform tasks
   - Combines reasoning and acting
   - Applications beyond chatbots

2. **API Management is Critical**
   - Multiple providers = backup plans
   - Rate limiting = need strategies
   - Documentation = save time

3. **UX Matters**
   - Small improvements = big impact
   - Pending state = professional feel
   - Auto-clear = smooth experience

4. **Persistence Pays Off**
   - API config took many tries
   - Tool integration had many issues
   - But systematic approach worked

### What Em Would Do Differently:

1. **Start with simpler API** for initial testing
2. **Implement unit tests** earlier in development
3. **Document more** while writing code
4. **Test edge cases** more thoroughly

## Conclusion

Em cảm thấy rất may mắn được làm project này. Em đã học rất nhiều về LLM agents, ReAct pattern, API integration, và UI/UX design.

Hài lòng về việc:
- Config MIMO API thành công sau nhiều thử nghiệm
- Help implement ReAct agent với 7 tools
- Improve UI with modern design


