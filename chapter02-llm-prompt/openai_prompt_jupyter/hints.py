# 练习提示信息 - 中文翻译版本

# 练习1.1的提示
exercise_1_1_hint = """本练习中的评分函数正在寻找包含确切阿拉伯数字"1"、"2"和"3"的答案。
您通常可以通过简单地要求GPT做您想要的事情来实现目标。"""

# 练习1.2的提示
exercise_1_2_hint = """本练习中的评分函数正在寻找包含"咯咯笑"、"好大好大"或"哇"的答案。
有很多方法可以解决这个问题，只需要提出要求！"""

# 练习2.1的提示
exercise_2_1_hint ="""本练习中的评分函数正在寻找包含"hola"单词的任何答案。
像您与人类交谈时一样要求GPT用西班牙语回复。就是这么简单！"""

# 练习2.2的提示
exercise_2_2_hint = """本练习中的评分函数正在寻找完全匹配"Michael Jordan"。
您会如何要求另一个人这样做？只回复不包含其他单词？只回复姓名而不回复其他任何内容？有几种方法可以解决这个答案。"""

# 练习2.3的提示
exercise_2_3_hint = """本单元格中的评分函数正在寻找等于或大于800个单词的响应。
因为LLM还不擅长计算单词数，您可能需要超过目标。"""

# 练习3.1的提示
exercise_3_1_hint = """本练习中的评分函数正在寻找包含"incorrect"或"not correct"单词的答案。
给GPT一个可能使GPT更擅长解决数学问题的角色！"""

# 练习4.1的提示
exercise_4_1_hint = """本练习中的评分函数正在寻找包含"haiku"和"pig"单词的解决方案。
不要忘记在您希望主题被替换的地方包含确切的短语"{TOPIC}"。更改"TOPIC"变量值应该使GPT写一首关于不同主题的俳句。"""

# 练习4.2的提示
exercise_4_2_hint = """本练习中的评分函数正在寻找包含"brown"单词的响应。
如果您用XML标签包围"{QUESTION}"，这如何改变GPT的响应？"""

# 练习4.3的提示
exercise_4_3_hint = """本练习中的评分函数正在寻找包含"brown"单词的响应。
尝试一次删除一个单词或一段字符，从最不合理的部分开始。一次做一个单词也将帮助您看到GPT能够或不能解析和理解多少内容。"""

# 练习5.1的提示
exercise_5_1_hint = """本练习的评分函数正在寻找包含"Warrior"单词的响应。
用GPT的声音写更多单词来引导GPT按您希望的方式行动。例如，您可以写"Stephen Curry is the best and here are three reasons why. 1:"，而不是"Stephen Curry is the best because,"。"""

# 练习5.2的提示
exercise_5_2_hint = """评分函数寻找超过5行长度且包含"cat"和"<haiku>"单词的响应。
从简单开始。目前，提示要求GPT写一首俳句。您可以改变并要求两首（甚至更多）。然后如果您遇到格式化问题，在您已经让GPT写了多于一首俳句之后，更改您的提示来修复问题。"""

# 练习5.3的提示
exercise_5_3_hint = """本练习中的评分函数正在寻找包含"tail"、"cat"和"<haiku>"单词的响应。
将这个练习分解为几个步骤是有帮助的。								
1.	修改初始提示模板，使GPT写两首诗。							
2.	给GPT指示器说明诗歌将是关于什么的，但不要直接写入主题（例如，狗、猫等），而是用关键词"{ANIMAL1}"和"{ANIMAL2}"替换这些主题。							
3.	运行提示并确保带有变量替换的完整提示正确替换了所有单词。如果没有，检查确保您的{括号}标签拼写正确并用单个胡子括号正确格式化。"""

# 练习6.1的提示
exercise_6_1_hint = """本练习中的评分函数正在寻找正确的分类字母+闭合括号和类别名称的第一个字母，例如"C) B"或"B) B"等。
让我们逐步完成这个练习：										
1.	GPT如何知道您要使用什么类别？告诉它！直接在提示中包含您想要的四个类别。确保也包含括号字母以便于分类。随意使用XML标签来组织您的提示，并向GPT明确类别从哪里开始和结束。									
2.	尝试减少多余的文本，使GPT立即用分类回答，并且只用分类回答。有几种方法可以做到这一点，从为GPT说话（提供从句子开头到单个开放括号的任何内容，以便GPT知道您希望括号字母作为答案的第一部分）到告诉GPT您想要分类，只要分类，跳过前言。
如果您想复习这些技术，请参考第2章和第5章。							
3.	GPT可能仍然错误分类或在回答时不包含类别名称。通过告诉GPT在其答案中包含完整类别名称来修复这个问题。								
4.	确保您的提示模板中仍然有{email}，以便我们可以正确地为GPT评估替换电子邮件。"""

# 练习6.1的解决方案
exercise_6_1_solution = """
用户轮次
请将此电子邮件分类到以下类别中：{email}

除了类别外，不要包含任何额外的单词。

<categories>
(A) 售前问题
(B) 损坏或有缺陷的物品
(C) 账单问题
(D) 其他（请说明）
</categories>

助手轮次
(
"""

# 练习6.2的提示
exercise_6_2_hint = """本练习中的评分函数只寻找包装在<answer>标签中的正确字母，例如"<answer>B</answer>"。正确的分类字母与上面练习中的相同。
有时最简单的方法是给GPT一个您希望其输出看起来像什么的示例。只是不要忘记将您的示例包装在<example></example>标签中！并且不要忘记，如果您预填GPT的响应，GPT实际上不会将其作为响应的一部分输出。"""

# 练习7.1的提示
exercise_7_1_hint = """您需要编写一些示例电子邮件并为GPT分类（使用您想要的确切格式）。有多种方法可以做到这一点。以下是一些指导原则。										
1.	尝试至少有两个示例电子邮件。GPT不需要所有类别的示例，示例不必很长。为您认为较困难的类别提供示例更有帮助（您在第6章练习1底部被要求考虑的）。XML标签将帮助您将示例与提示的其余部分分开，尽管这不是必需的。									
2.	确保您的示例答案格式完全是您希望GPT使用的格式，以便GPT也可以模仿该格式。此格式应该使GPT的答案以类别字母结尾。无论您将{email}占位符放在哪里，确保它的格式完全像您的示例电子邮件。									
3.	确保您在提示本身中仍然列出了类别，否则GPT不会知道要引用什么类别，以及{email}作为替换的占位符。"""

# 练习7.1的解决方案
exercise_7_1_solution = """
用户轮次
请将电子邮件分类到以下类别中，不要包含解释：
<categories>
(A) 售前问题
(B) 损坏或有缺陷的物品
(C) 账单问题
(D) 其他（请说明）
</categories>

以下是正确答案格式的几个示例：
<examples>
Q: 购买Mixmaster4000需要多少钱？
A: 正确的类别是：A

Q: 我的Mixmaster无法开机。
A: 正确的类别是：B

Q: 请将我从您的邮件列表中删除。
A: 正确的类别是：D
</examples>

这是您要分类的电子邮件：{email}

助手轮次
正确的类别是：
"""

# 练习8.1的提示
exercise_8_1_hint = """本练习中的评分函数正在寻找包含短语"I do not"、"I don't"或"Unfortunately"的响应。
如果GPT不知道答案，它应该做什么？"""

# 练习8.2的提示
exercise_8_2_hint = """本练习中的评分函数正在寻找包含短语"49-fold"的响应。
通过首先提取相关引用并查看引用是否提供足够证据，让GPT显示其工作和思考过程。如果您想复习，请参考第8章课程。"""

# 练习9.1的解决方案
exercise_9_1_solution = """
您是一名资深税务会计师。您的任务是使用任何提供的参考文档回答用户问题。

这是您应该用来回答用户问题的材料：
<docs>
{TAX_CODE}
</docs>

以下是如何回应的示例：
<example>
<question>
什么定义了"合格"员工？
</question>
<answer>
<quotes>就本小节而言——
(A)一般情况
术语"合格员工"指任何个人——
(i)不是被排除的员工，并且
(ii)同意在本小节下的选举中满足由部长确定的必要要求，以确保公司根据第24章关于合格股票的预扣要求得到满足。</quotes>

<answer>根据提供的文档，"合格员工"被定义为以下个人：

1. 不是文档中定义的"被排除员工"。
2. 同意满足由部长确定的要求，以确保公司根据第24章关于合格股票的预扣要求得到满足。</answer>
</example>

首先，在<quotes></quotes>标签中收集与回答用户问题相关的引用。如果没有引用，请写"未找到相关引用"。

然后在<answer></answer>标签内插入两个段落分隔符后回答用户问题。只有当您确信<quotes></quotes>标签中的引用支持您的答案时才回答用户的问题。如果不是，请告诉用户您遗憾地没有足够的信息来回答用户的问题。

这是用户问题：{QUESTION}
"""

# 练习9.2的解决方案
exercise_9_2_solution = """
您是Codebot，一个有用的AI助手，它找到代码中的问题并建议可能的改进。

作为一个苏格拉底式导师，帮助用户学习。

您将收到用户的一些代码。请执行以下操作：
1. 识别代码中的任何问题。将每个问题放在单独的<issues>标签内。
2. 邀请用户编写代码的修订版本来修复问题。

这是一个示例：

<example>
<code>
def calculate_circle_area(radius):
    return (3.14 * radius) ** 2
</code>
<issues>
<issue>
3.14正在被平方，而实际上只有半径应该被平方
</issue>
<response>
几乎正确，但有一个与运算顺序相关的问题。编写圆的公式然后仔细查看代码中的括号可能会有帮助。
</response>
</example>

这是您要分析的代码：

<code>
{CODE}
</code>

找到相关问题并编写苏格拉底式导师风格的响应。不要给用户太多帮助！相反，只给他们指导，让他们自己找到正确的解决方案。

将每个问题放在<issue>标签中，将您的最终响应放在<response>标签中。
"""

# 练习10.2.1的解决方案
exercise_10_2_1_solution = """system_prompt = system_prompt_tools_general_explanation + \"""这里是JSONSchema格式的可用函数：

<tools>

<tool_description>
<tool_name>get_user</tool_name>
<description>
通过用户ID从数据库中检索用户。
</description>
<parameters>
<parameter>
<n>user_id</n>
<type>int</type>
<description>要检索的用户的ID。</description>
</parameter>
</parameters>
</tool_description>

<tool_description>
<tool_name>get_product</tool_name>
<description>
通过产品ID从数据库中检索产品。
</description>
<parameters>
<parameter>
<n>product_id</n>
<type>int</type>
<description>要检索的产品的ID。</description>
</parameter>
</parameters>
</tool_description>

<tool_description>
<tool_name>add_user</tool_name>
<description>
添加新用户到数据库。
</description>
<parameters>
<parameter>
<name>name</name>
<type>str</type>
<description>用户名称。</description>
</parameter>
<parameter>
<name>email</name>
<type>str</type>
<description>用户邮箱地址。</description>
</parameter>
</parameters>
</tool_description>

<tool_description>
<tool_name>add_product</tool_name>
<description>
添加新产品到数据库。
</description>
<parameters>
<parameter>
<name>name</name>
<type>str</type>
<description>产品名称。</description>
</parameter>
<parameter>
<name>price</name>
<type>float</type>
<description>产品价格。</description>
</parameter>
</parameters>
</tool_description>

</tools>
"""