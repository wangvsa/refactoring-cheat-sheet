## 合并条件式
---

你有一系列条件测试，都得到相同结果。
**将这些测试合并为一个条件式，并将这个条件式提炼成为一个独立函数。**

```java
double disabilityAmount() {
    if (_seniority < 2) return 0;
    if (_monthsDisabled > 12) return 0;
    if (_isPartTime) return 0;
    // compute the disability amount
```

![](/images/arrow.gif)

```java
double disabilityAmount() {
    if (isNotEligableForDisability()) return 0;
    // compute the disability amount
```

**动机（Motivation）**

有时你会发现这样一串条件检查：检查条件各不相同，最终行为却一致。如果发现这种情况，就应该使用logical-AND 和logical-OR 将它们合并为一个条件式。

之所以要合并条件代码，有两个重要原因。首先，合并后的条件代码会告诉你「实际上只有一次条件检查，只不过有数个并列条件需要检查而已」，从而使这一次检查的用意更清晰。当然，合并前和合并后的代码有着相同的效果，但原先代码传达出的信息却是「这里有一些独立条件测试，它们只是恰好同时发生」。其次，这项重构往往可以为你使用 [提炼函数](composing-methods.md#_1) 做好准备。「将检查条件提炼成一个独立函数」对于厘清代码意义非常有用，因为它把描述「做什么」的语句换成了「为什么这样做」。

条件语句的「合并理由」也同时指出了「不要合并」的理由。如果你认为这些检查的确彼此独立，的确不应该被视为同一次检查，那么就不要使用本项重构。因为在 这种情况下，你的代码己经清楚表达出自己的意义。

**作法（Mechanics）**

- 确定这些条件语句都没有副作用（连带影响）。
    - 如果条件式有副作用，你就不能使用本项重构。
- 使用适当的逻辑操作符（logical operators），将一系列相关条件式合并为一个。
- 编译，测试。
- 对合并后的条件式实施[提炼函数](composing-methods.md#_1)。


**范例：Ors**


请看下列代码：

```java
double disabilityAmount() {
    if (_seniority < 2) return 0;
    if (_monthsDisabled > 12) return 0;
    if (_isPartTime) return 0;
    // compute the disability amount
    ...
```
 

在这段代码中，我们看到一连串的条件检查，它们都做同一件事。对于这样的代码， 上述条件检查等价于一个以"logical-OR"连接起来的语句：

```java
double disabilityAmount() {
    if ((_seniority < 2) || (_monthsDisabled > 12) || (_isPartTime)) return 0;
    // compute the disability amount
    ...
```


现在，我可以观察这个新的条件式，并运用[提炼函数](composing-methods.md#_1) 将它提炼成一个独立函数，以函数名称表达该语句所检查的条件：

```java
double disabilityAmount() {
    if (isNotEligibleForDisability()) return 0;
    // compute the disability amount
    ...
}

boolean isNotEligibleForDisability() {
    return ((_seniority < 2) || (_monthsDisabled > 12) || (_isPartTime));
}
```
 
**范例：Ands**

上述实例展示了"logical-OR"的用法。下列代码展示"logical-AND"的用法：

```java
if (onVacation())
    if (lengthOfService() > 10)
        return 1;
    return 0.5;
```


这段代码可以变成：

```java
if (onVacation() && lengthOfService() > 10) return 1;
else return 0.5;
```


你可能还会发现，某些情况下需要同时使用logical-AND、logical-OR 和 logical-NOT，最终得到的条件式可能很复杂，所以我会先使用[提炼函数](composing-methods.md#_1) 将表达式的一部分提炼出来，从而使整个表达式变得简单一些。


如果我所观察的部分，只是对条件进行检查并返回一个值，我可以使用三元操作符将这一部分变成一条return 语句。因此，下列代码：

```java
if (onVacation() && lengthOfService() > 10) return 1;
else return 0.5;
```

就变成了：

```java
return (onVacation() && lengthOfService() > 10) ? 1 : 0.5;
```


## 合并重复的条件片段
---

在条件式的每个分支上有着相同的一段代码。

**将这段重复代码搬移到条件式之外。**

```java
if (isSpecialDeal()) {
    total = price * 0.95;
    send();
}
else {
    total = price * 0.98;
    send();
}
```

![](/images/arrow.gif)

```java
if (isSpecialDeal())
    total = price * 0.95;
else
    total = price * 0.98;
send();
```

**动机（Motivation）**

有时你会发现，一组条件式的所有分支都执行了相同的某段代码。如果是这样，你就应该将这段代码搬移到条件式外面。这样，代码才能更清楚地表明哪些东西随条件的变化而变化、哪些东西保持不变。

**作法（Mechanics）**

  - 鉴别出「执行方式不随条件变化而变化」的代码。
  - 如果这些共通代码位于条件式起始处，就将它移到条件式之前。
  - 如果这些共通代码位于条件式尾端，就将它移到条件式之后。
  - 如果这些共通代码位于条件式中段，就需要观察共通代码之前或之后的代码 是否改变了什么东西。如果的确有所改变，应该首先将共通代码向前或向后 移动，移至条件式的起始处或尾端，再以前面所说的办法来处理。
  - 如果共通代码不止一条语句，你应该首先使用以[提炼函数](composing-methods.md#_1) 将共通 代码提炼到一个独立函数中，再以前面所说的办法来处理。


**范例：（Example）**

你可能遇到这样的代码：

```java
if (isSpecialDeal()) {
    total = price * 0.95;
    send();
}
else {
    total = price * 0.98;
    send();
}
```


由于条件式的两个分支都执行了 send() 函数，所以我应该将send() 移到条件式的外围：

```java
if (isSpecialDeal())
    total = price * 0.95;
else
    total = price * 0.98;
send();
```


我们也可以使用同样的手法来对待异常（exceptions）。如果在try 区段内「可能引发异常」的语句之后，以及所有catch 区段之内，都重复执行了同一段代码，我就 可以将这段重复代码移到final 区段。


## 分解条件式
---

在条件式的每个分支上有着相同的一段代码。
**将这段重复代码搬移到条件式之外。**
 
```java
if (isSpecialDeal()) {
    total = price * 0.95;
    send();
}
else {
    total = price * 0.98;
    send();
}
```

![](/images/arrow.gif)

```java
if (isSpecialDeal())
    total = price * 0.95;
else
    total = price * 0.98;
send();
```

**动机（Motivation）**

有时你会发现，一组条件式的所有分支都执行了相同的某段代码。如果是这样，你就应该将这段代码搬移到条件式外面。这样，代码才能更清楚地表明哪些东西随条件的变化而变化、哪些东西保持不变。

**作法（Mechanics）**

  - 鉴别出「执行方式不随条件变化而变化」的代码。
  - 如果这些共通代码位于条件式起始处，就将它移到条件式之前。
  - 如果这些共通代码位于条件式尾端，就将它移到条件式之后。
  - 如果这些共通代码位于条件式中段，就需要观察共通代码之前或之后的代码 是否改变了什么东西。如果的确有所改变，应该首先将共通代码向前或向后 移动，移至条件式的起始处或尾端，再以前面所说的办法来处理。
  - 如果共通代码不止一条语句，你应该首先使用以[提炼函数](composing-methods.md#_1) 将共通 代码提炼到一个独立函数中，再以前面所说的办法来处理。


**范例：（Example）**

你可能遇到这样的代码：
```java
if (isSpecialDeal()) {
    total = price * 0.95;
    send();
}
else {
    total = price * 0.98;
    send();
}
```


由于条件式的两个分支都执行了 send() 函数，所以我应该将send() 移到条件式的外围：
```java
if (isSpecialDeal())
    total = price * 0.95;
else
    total = price * 0.98;
send();
```
 

我们也可以使用同样的手法来对待异常（exceptions）。如果在try 区段内「可能引发异常」的语句之后，以及所有catch 区段之内，都重复执行了同一段代码，我就 可以将这段重复代码移到final 区段。

## 引入断言
---

某一段代码需要对程序状态（state）做出某种假设。

**以assertion（断言）明确表现这种假设。**

```java
double getExpenseLimit() {
    // should have either expense limit or a primary project
    return (_expenseLimit != NULL_EXPENSE) ?
        _expenseLimit:_primaryProject.getMemberExpenseLimit();
}
```

![](/images/arrow.gif)

```java
double getExpenseLimit() {
    Assert.isTrue (_expenseLimit != NULL_EXPENSE || _primaryProject != null);
    return (_expenseLimit != NULL_EXPENSE) ?
        _expenseLimit: _primaryProject.getMemberExpenseLimit();
}
```

**动机（Motivation）**

常常会有这样一段代码：只有当某个条件为真时，该段代码才能正常运行。例如「平方报计算」只对正值才能进行（译注：这里没考虑复数与虚数），又例如某个对象 可能假设其值域（fields）至少有一个不等于null。

这样的假设通常并没有在代码中明确表现出来，你必须阅读整个算法才能看出。有时程序员会以注释写出这样的假设。而我要介绍的是一种更好的技术：使用assertion（断言）明确标明这些假设。

assertion 是一个条件式，应该总是为真。如果它失败，表示程序员犯了错误。因此assertion的失败应该导致一个unchecked exception 7（不可控异常〕。Assertions 绝对不能被系统的其他部分使用。实际上程序最后成品往往将assertions 统统删除。因此，标记「某些东西是个assertion」是很重要的。

7译注：所谓unchecked exception 是指「未曾于函数签名式（signature）中列出」的异常。

Assertions 可以作为交流与调试的辅助。在交流（沟通〕的角度上，assertions 可以帮助程序阅读者理解代码所做的假设；在调试的角度上，assertions 可以在距离「臭虫」最近的地方抓住它们。当我编写自我测试代码的时候，我发现，assertions 在调试方面的帮助变得不那么重要了，但我仍然非常看重它们在交流方面的价值。

**作法（Mechanics）**

如果程序员不犯错，assertions 就应该不会对系统运行造成任何影响，所以加入assertions 永远不会影响程序的行为。

- 如果你发现代码「假设某个条件始终（必须）为真]，就加入一个assertion 明确说明这种情况。
    - 你可以新建一个Assert class，用于处理各种情况下的assertions 。


注意，不要滥用assertions 。请不要使用它来检查你「认为应该为真」的条件，请只使用它来检查「一定必须为真」的条件。滥用assertions 可能会造成难以维护的重复逻辑。在一段逻辑中加入assertions 是有好处的，因为它迫使你重新考虑这段代 码的约束条件。如果「不满足这些约朿条件，程序也可以正常运行」，assertions 就不会带给你任何帮助，只会把代码变得混乱，并且有可能妨碍以后的修改。

你应该常常问自己：如果assertions 所指示的约束条件不能满足，代码是否仍能正常运行？如果可以，就把assertions 拿掉。

另外，还需要注意assertions 中的重复代码。它们和其他任何地方的重复代码一样不好闻。你可以大胆使用[提炼函数](composing-methods.md#_1) 去掉那些重复代码。

**范例：（Example）**

下面是一个简单例子：开支（经费）限制。后勤部门的员工每个月有固定的开支限额；业务部门的员工则按照项目的开支限额来控制自己的开支。一个员工可能没有开支额度可用，也可能没有参与项目，但两者总得要有一个（否则就没有经费可用 了）。在开支限额相关程序中，上述假设总是成立的，因此：

```java
class Employee...
    private static final double NULL_EXPENSE = -1.0;
    private double _expenseLimit = NULL_EXPENSE;
    private Project _primaryProject;
    double getExpenseLimit() {
        return (_expenseLimit != NULL_EXPENSE) ?
        _expenseLimit:
        _primaryProject.getMemberExpenseLimit();
    }
    boolean withinLimit (double expenseAmount) {
        return (expenseAmount <= getExpenseLimit());
    }
```


这段代码包含了一个明显假设：任何员工要不就参与某个项目，要不就有个人开支限额。我们可以使用assertion 在代码中更明确地指出这一点：
```java
double getExpenseLimit() {
    Assert.isTrue (_expenseLimit != NULL_EXPENSE || _primaryProject != null);
    return (_expenseLimit != NULL_EXPENSE) ? _expenseLimit:_primaryProject.getMemberExpenseLimit();
}
```


这条assertion 不会改变程序的任何行为。另一方面，如果assertion中的条件不为真，我就会收到一个运行期异常：也许是在withinLimit() 函数中抛出一个空指针（null pointer）异常，也许是在Assert.isTrue() 函数中抛出一个运行期异常。有时assertion 可以帮助程序员找到臭虫，因为它离出错地点很近。但是，更多时候，assertion 的价值在于：帮助程序员理解代码正确运行的必要条件。


我常对assertion 中的条件式使用[提炼函数](composing-methods.md#_1) ，也许是为了将若干地方的重复码提炼到同一个函数中，也许只是为了更清楚说明条件式的用途。


在Java 中使用assertions 有点麻烦：没有一种简单机制可以协助我们插入这东西8。 assertions 可被轻松拿掉，所以它们不可能影响最终成品的性能。编写一个辅助类（例如Assert class）当然有所帮助，可惜的是assertions 参数中的任何表达式不论什么情况都一定会被执行一遍。阻止它的惟一办法就是使用类似下面的手法：


8译注：J2SE1.4已经支持assert语句。

```java
double getExpenseLimit() {
    Assert.isTrue (Assert.ON && (_expenseLimit != NULL_EXPENSE || _primaryProject != null));
    return (_expenseLimit != NULL_EXPENSE) ?
        _expenseLimit:_primaryProject.getMemberExpenseLimit();
}
```


或者是这种手法：

```java
double getExpenseLimit() {
    if (Assert.ON)
        Assert.isTrue (_expenseLimit != NULL_EXPENSE || _primaryProject != null);
    return (_expenseLimit != NULL_EXPENSE) ?
        _expenseLimit:_primaryProject.getMemberExpenseLimit();
}
```


如果Assert.ON 是个常量，编译器（译注：而非运行期间）就会对它进行检查； 如果它等于false ，就不再执行条件式后半段代码。但是，加上这条语句实在有点丑陋，所以很多程序员宁可仅仅使用Assert.isTrue() 函数，然后在项目结束前以过滤程序滤掉使用assertions 的每一行代码（可以使用Perl 之类的语言来编写这样 的过滤程序）。

Assert class应该有多个函数，函数名称应该帮助程序员理解其功用。除了isTrue() 之外，你还可以为它加上equals() 和shouldNeverReachHere() 等函数。

## 引入Null对象
---

你需要再三检查「某物是否为null value」。
**将null value （无效值）替换为null object（无效物）。**

```java
if (customer == null) plan = BillingPlan.basic();
else plan = customer.getPlan();
```

![](/images/arrow.gif)

![](/images/09fig01b.gif)

**动机（Motivation）**

多态（polymorphism ）的最根本好处在于：你不必再向对象询问「你是什么型别」 而后根据得到的答案调用对象的某个行为——你只管调用该行为就是了，其他的一切多态机制会为你安排妥当。当你的某个值域内容是null value 时，多态可扮演另一个较不直观（亦较不为人所知）的用途。让我们先听听Ron Jeffries 的故事。

<blockquote>

Ron Jeffries

我们第一次使用Null Object 模式，是因为Rih Garzaniti 发现，系统在对对象发送一个消息之前，总要检査对象是否存在，这样的检査出现很多次。我们可能会向一个对象索求它所相关的Person 对象，然后再问那个对象是否为null 。如果对象的确存在，我们才能调用它的rate() 函数以查询这个人的薪资级别。我们在好些地方都是这样做的， 造成的重复代码让我们很烦心。

所以.我们编写了一个MissingPerson class，让它返回 '0' 薪资等级（我们把null objects 称为missing object（虚构对象）。很快地MissingPerson 就有了很多函数，rate() 自然是其中之一。如今我们的系统有超过80个null object classes。

我们常常在显示信息的时候使用null object。例如我们想要显示一个Person 对象信息，它大约有20个instance 变量。如果这些变量可被设为null，那么打印一个Person 对象的工作将非常复杂。所以我们不让instance 变量被设为null ，而是插入各式各样的null objects ——它们都知道如何正常（正确地）显示自己。这样，我们就可以摆脱大量代码。

我们对null object 的最聪明运用，就是拿它来表示不存在的Gemstone session。我们使用Gemstone 数据库来保存成品（程序代码），但我们更愿息在没有数据库的情况下进行开发，毎过一周左右再把新码放进Gemstone 数据库。然而在代码的某些地方，我们必须登录（log in）一个Gemstone session。当我们没有Gemstone 数据库时，我们就仅仅安插一个miss Gemstone session，其接口和真正的Gemstone session 一模一样，使我们无需判断数据库是否存在，就可以进行开发和测试。

null object 的另一个用途是表现出「虚构的箱仓」（missing bin）。所谓「箱仓]，这里是指群集（collection），用来保存某些薪资值，并常常谣要对各个薪资值进行加和或遍历。如果某个箱仓不存在，我们就给出一个虚构的箱仓对象，其行为和一个空箱仓（empty bin）一样；这个虚构箱仓知道自己其实不带任何数据，总值为0。通过这种作法，我们就不必为上千位员工每人产生数十来个空箱（empty bins）对象了。

使用null objects 有个非常有趣的性质：好事绝对不会因为null objects 而「被破坏」。由于null objects 对所有外界请求的响应，都像real objects 的响应一样，所以系统行为总是正常的。但这并非总是好事，有吋会造成问题的侦测和查找上的困难，因为从来没有任何东西被破坏。当然，只要认真检查一下，你就会发现null objects 有时出现在不该出现的地方。

请记住：null objects 一定是常量，它们的任何成分都不会发生变化。因此我们可以使用Singleton 模式[Gang of Four]来实现它们。例如不管任何时候，只要你索求一个MissingPerson 对象，你得到的一定是MissingPerson 的惟一实体。
</blockquote>


关于Null Object 模式，你可以在Woolf [Woolf] 中找到更详细的介绍。

**作法（Mechanics）**

- 为source class 建立一个subclass ，使其行为像source class 的null 版本。在source class 和null class 中都加上isNull() 函数，前者的isNull() 应该返回false，后者的isNull() 应该返回true。
- 下面这个办法也可能对你有所帮助：建立一个nullable 接口，将isNull() 函数放在其中，让source class 实现这个接口。
- 另外，你也可以创建一个testing 接口，专门用来检查对象是否为null。
- 编译。
- 找出所有「索求source object 却获得一个null 」的地方。修改这些地方，使它们改而获得一个null object。
- 找出所有「将source object 与null 做比较」的地方。修改这些地方，使它们调用isNull() 函数。
- 你可以每次只处理一个source object 及其客户程序，编译并测试后， 再处理另一个source object 。
- 你可以在「不该再出现null value」的地方放上一些assertions（断言）， 确保null 的确不再出现。这可能对你有所帮助。
  - 编译，测试。
  - 找出这样的程序点：如果对象不是null ，做A动作，否则做B 动作。
  - 对于每一个上述地点，在null class 中覆写A动作，使其行为和B 动作相同。
  - 使用上述的被覆写动作（A），然后删除「对象是否等于null」的条件测试。编译并测试。


**范例：（Example）**

—家公用事业公司的系统以Site 表示地点（场所）。庭院宅等和集合公寓（apartment）都使用该公司的服务。任何时候每个地点都拥有（或说都对应于）一个顾客，顾客信息以Customer 表示：

```java
class Site...
    Customer getCustomer() {
        return _customer;
    }
    Customer _customer;
```


Customer 有很多特性，我们只看其中三项：
```java
class Customer...
    public String getName() {...}
    public BillingPlan getPlan() {...}
    public PaymentHistory getHistory() {...}
```


本系统又以PaymentHistory 表示顾客的付款记录，它也有它自己的特性：

```java
public class PaymentHistory...
    int getWeeksDelinquentInLastYear()
```


上面的各种取值函数（getter）允许客户取得各种数据。但有时候一个地点的顾客搬走了，新顾客还没搬进来，此时这个地点就没有顾客。由于这种情况有可能发生，所以我们必须保证Customer 的所有用户都能够处理「Customer 对象等于null」的情况。下面是一些示例片段：

```java
Customer customer = site.getCustomer();
BillingPlan plan;
if (customer == null) plan = BillingPlan.basic();
else plan = customer.getPlan();
...
String customerName;
if (customer == null) customerName = "occupant";
else customerName = customer.getName();
...
int weeksDelinquent;
if (customer == null) weeksDelinquent = 0;
else weeksDelinquent = customer.getHistory().getWeeksDelinquentInLastYear();
```


这个系统中可能使用许多Site 和Customer ，它们都必须检查Customer 对象是否等于null ，而这样的检查完全是重复的。看来是使用null object 的时候了。

首先新建一个NullCustomer ，并修改Customer ，使其支持「对象是否为null」的检查：

```java
class NullCustomer extends Customer {
    public boolean isNull() {
        return true;
    }
}

class Customer...
    public boolean isNull() {
        return false;
    }

    protected Customer() {} //needed by the NullCustomer
```


如果你无法修改Customer ，你可以建立一个新的testing 接口。


如果你喜欢，也可以新建一个接口，昭告大家「这里使用了null object 」：

```java
interface Nullable {
    boolean isNull();
}

class Customer implements Nullable
```


我还喜欢加入一个factory method，专门用来创建NullCustomer 对象。这样一来，用户就不必知道null class 的存在了：

```java
class Customer...
    static Customer newNull() {
        return new NullCustomer();
    }
```


接下来的部分稍微有点麻烦。对于所有「返回null」的地方，我都要将它改为「返回null object」，此外我还要把foo==null这样的检查替换成foo.isNull()。我发现下列办法很有用：查找所有『索求Customer 对象」的地方，将它们都加以修改, 使它们不能返回null ，改而返回一个NullCustomer 对象。

```java
class Site...
    Customer getCustomer() {
        return (_customer == null) ? Customer.newNull():_customer;
    }
```


另外，我还要修改所有「使用Customer 对象」的地方，让它们以isNull() 函数进行检查，不再使用"== null"”检查方式。

```java
Customer customer = site.getCustomer(); 
BillingPlan plan;
if (customer.isNull()) plan = BillingPlan.basic();
else plan = customer.getPlan();
...
String customerName;
if (customer.isNull()) customerName = "occupant";
else customerName = customer.getName();
...
int weeksDelinquent;
if (customer.isNull()) weeksDelinquent = 0;
else weeksDelinquent = customer.getHistory().getWeeksDelinquentInLastYear();
```


毫无疑问，这是本项重构中最需要技巧的部分。对于每一个需要替换的「可能等于null」的对象，我都必须找到「它是否等于null」的所有检查动作，并逐一替换。 如果这个对象被传播到很多地方，追踪起来就很困难。上述范例中，我必须找出每一个型别为Customer 的变量，以及它们被使用的地点。很难将这个过程分成更小的步骤。有时候我发现「可能等于null」的对象只在某几处被用到，那么替换工作比较简单。但是大多数时候我必须做大量替换工作。还好，撤销这些替换并不困难，因为我可以不太困难地找出对isNull() 的调用动作，但这毕竟也是很零乱很恼人 的。


这个步骤完成之后，如果编译和测试都顺利通过，我就可以宽心地露出笑容了。接下来的动作比较有趣。到目前为止，使用isNull() 函数尚未带来任何好处。只有当我把相关行为移到NullCustomer class 中并去除条件式之后，我才能得到切实的利益。我可以逐一将各种行为（函数）移过去。首先从「取得顾客名称」这个函数开始。此时的客户端代码大约如下：

```java
String customerName;
if (customer.isNull()) customerName = "occupant";
else customerName = customer.getName();
```


首先为NullCustomer 加入一个合适的函数，通过这个函数来取得顾客名称：

```java
class NullCustomer...
    public String getName(){
        return "occupant";
    }
```


现在，我可以去掉条件代码了：

```java
String customerName = customer.getName();
```


接下来我以相同手法处理其他函数，使它们对相应查询做出合适的响应。此外我还可以对「修改函数」（modifiers）做适当的处理。于是下面这样的客户端程序：

```java
if (! customer.isNull())
    customer.setPlan(BillingPlan.special());
```


就变成了这样：

```java
customer.setPlan(BillingPlan.special());

class NullCustomer...
    public void setPlan (BillingPlan arg) {}
```


请记住：只有当大多数客户代码都要求null object 做出相同响应时，这样的行为搬移才有意义。注意我说的是「大多数」而不是「所有」。任何用户如果需要null object 作出不同响应，他仍然可以使用isNull() 函数来测试。只要大多数客户端都要求null object 做出相同响应，他们就可以调用缺省的null 行为，而你也就受益匪浅了。

上述范例略带差异的某种情况是，某些客户端使用Customer 函数的运算结果：

```java
if (customer.isNull()) weeksDelinquent = 0;
else weeksDelinquent = customer.getHistory().getWeeksDelinquentInLastYear();
```


我可以新建一个NullPaymentHistory class，用以处理这种情况：

```java
class NullPaymentHistory extends PaymentHistory...
    int getWeeksDelinquentInLastYear() {
        return 0;
    }
```


并修改NullCustomer，让它返回一个NullPaymentHistory 对象：

```java
class NullCustomer...
    public PaymentHistory getHistory() {
        return PaymentHistory.newNull();
    }
```


然后，我同样可以删除这一行条件代码：

```java
int weeksDelinquent = customer.getHistory().getWeeksDelinquentInLastYear();
```


你常常可以看到这样的情况：null objects 会返回其他null objects 。

**范例：另一种做法，Testing Interface**

除了定义isNull() 之外，你也可以建立一个用以检查「对象是否为null」的接口。 使用这种办法，必须新建一个Null 接口，其中不定义任何函数：

```java
interface Null {}
```


然后，让null object 实现Null 接口：

```java
class NullCustomer extends Customer implements Null...
```


然后，我就可以用instanceof 操作符检查对象是否为null ：

```java
aCustomer instanceof Null
```


通常我尽量避免使用instanceof 操作符，但在这种情况下，使用它是没问题的。而且这种作法还有另一个好处：不需要修改Customer 。这么一来即使无法修改Customer 源码，我也可以使用null object 。

**其他特殊情况**

使用本项重构时，你可以有数种不同的null objects ，例如你可以说「没有顾客」（新建的房子和暂时没人住的房子）和「不知名顾客」（有人住，但我们不知道是谁） 这两种情况是不同的。果真如此，你可以针对不同的情况建立不同的null class。有时候null objects 也可以携带数据，例如不知名顾客的使用记录等等，于是我们可以在查出顾客姓名之后将帐单寄给他。

本质上来说，这是一个比Null Object 模式更大的模式：Special Case 模式。所谓special case class（特例类）是某个class 的特殊情况，有着特殊的行为。因此表示「不知名顾客」的UnknowCustomer 和表示「没有顾客」的NoCustomer 都是Customer 的特例。你经常可以在表示数量的classes 中看到这样的「特例类」，例如Java 浮点数有「正无穷大」、「负无穷大」和「非数量」（NaN）等特例。special case class（特例类）的价值是：它们可以降低你的「错误处理」开销。例如浮点运算决不会抛出异常。如果你对NaN做浮点运算，结果也会是个NaN。这和「null object 的访问函数通常返回另一个null object 」是一样的道理。


## 移出控制标记
---

在一系列布尔表达式（boolean expressions）中，某个变量带有「控制标记」（control flag）的作用。
**以break 语句或return 的语句取代控制标记。**

**动机（Motivation）**

在一系列条件表达式中，你常常会看到「用以判断何时停止条件检查」的控制标记（control flag）：

```java
set done to false
while not done
    if (condition)
        do something
    set done to true
    next step of loop
```


这样的控制标记带来的麻烦超过了它所带来的便利。人们之所以会使用这样的控制标记，因为结构化编程原则告诉他们：每个子程序（routines）只能有一个入口（entry） 和一个出口（exit）。我赞同「单一入口」原则（而且现代编程语言也强迫我们这样做），但是「单一出口」原则会让你在代码中加入讨厌的控制标记，大大降低条件表达式的可读性。这就是编程语言提供break 语句和continue 语句的原因：你可以用它们跳出复杂的条件语句。去掉控制标记所产生的效果往往让你大吃一惊：条件语句真正的用途会清晰得多。

**作法（Mechanics）**

对控制标记（control flags）的处理，最显而易见的办法就是使用Java 提供的break 语句或continue 语句。

- 找出「让你得以跳出这段逻辑」的控制标记值。
- 找出「将可跳出条件式之值赋予标记变量」的那个语句，代以恰当的break 语句或continue 语句。
- 每次替换后，编译并测试。


在未能提供break 和continue 语句的编程语言中，我们可以使用另一种办法：

- 运用[提炼函数](composing-methods.md#_1)，将整段逻辑提炼到一个独立函数中。
- 找出「让你得以跳出这段逻辑」的那些控制标记值。
- 找出「将可跳出条件式之值赋予标记变量」的那个语句，代以恰当的return 语句。
- 每次替换后，编译并测试。



即使在支持break 和continue 语句的编程语言中，我通常也优先考虑上述第二方案。因为return 语句可以非常清楚地表示：不再执行该函数中的其他任何代码。 如果还有这一类代码，你早晚需要将这段代码提炼出来。

请注意标记变量是否会影响这段逻辑的最后结果。如果有影响，使用break 语句之后你还得保留控制标记值。如果你已经将这段逻辑提炼成一个独立函数，也可以将控制标记值放在return 语句中返回。

**范例：以break 取代简单的控制标记**

下列函数用来检查一系列人名之中是否包含两个可疑人物的名字（这两个人的名字硬编码于代码中〕：

```java
void checkSecurity(String[] people) {
    boolean found = false;
    for (int i = 0; i < people.length; i++) {
        if (! found) {
            if (people[i].equals ("Don")){
                sendAlert();
                found = true;
            }
            if (people[i].equals ("John")){
                sendAlert();
                found = true;
            }
        }
    }
}
```


这种情况下很容易找出控制标记：当变量found 被赋予true 时，搜索就结束。我可以逐一引入break 语句：

```java
void checkSecurity(String[] people) {
    boolean found = false;
    for (int i = 0; i < people.length; i++) {
        if (! found) {
            if (people[i].equals ("Don")){
                sendAlert();
                break;
            }
            if (people[i].equals ("John")){
                sendAlert();
                found = true;
            }
        }
    }
}
```


最后获得这样的成功：

```java
void checkSecurity(String[] people) {
    boolean found = false;
    for (int i = 0; i < people.length; i++) {
        if (! found) {
            if (people[i].equals ("Don")){
                sendAlert();
                break;
            }
            if (people[i].equals ("John")){
                sendAlert();
                break;
            }
        }
    }
}
```


然后我就可以把对控制标记的所有引用去掉：

```java
void checkSecurity(String[] people) {
    for (int i = 0; i < people.length; i++) {
        if (people[i].equals ("Don")){
            sendAlert();
            break;
        }
        if (people[i].equals ("John")){
            sendAlert();
            break;
        }
    }
}
```

**范例：以return 返回控制标记**

本项重构的另一种形式将使用return 语句。为了阐述这种用法，我把前面的例子稍加修改，以控制标记记录搜索结果：

```java
void checkSecurity(String[] people) {
    String found = "";
    for (int i = 0; i < people.length; i++) {
        if (found.equals("")) {
            if (people[i].equals ("Don")){
                sendAlert();
                found = "Don";
            }
            if (people[i].equals ("John")){
                sendAlert();
                found = "John";
            }
        }
    }
    someLaterCode(found);
}
```


在这里，变量found 做了两件事：它既是控制标记，也是运算结果。遇到这种情况，我喜欢先把计算found 变量的代码提炼到一个独立函数中：

```java
void checkSecurity(String[] people) {
    String found = foundMiscreant(people);
    someLaterCode(found);
}

String foundMiscreant(String[] people){
    String found = "";
    for (int i = 0; i < people.length; i++) {
        if (found.equals("")) {
            if (people[i].equals ("Don")){
                sendAlert();
                found = "Don";
            }
            if (people[i].equals ("John")){
                sendAlert();
                found = "John";
            }
        }
    }
    return found;
}
```


然后以return 语句取代控制标记：

```java
String foundMiscreant(String[] people){
    String found = "";
    for (int i = 0; i < people.length; i++) {
        if (found.equals("")) {
            if (people[i].equals ("Don")){
                sendAlert();
                return "Don";
            }
            if (people[i].equals ("John")){
                sendAlert();
                found = "John";
            }
        }
    }
    return found;
}
```


最后完全去掉控制标记：           

```java
String foundMiscreant(String[] people){
    for (int i = 0; i < people.length; i++) {
        if (people[i].equals ("Don")){
            sendAlert();
            return "Don";
        }
        if (people[i].equals ("John")){
            sendAlert();
            return "John";
        }
    }
    return "";
}
```


即使不需要返回某值，你也可以使用语句来取代控制标记。这时候你只需 要一个空的return 语句就行了。

当然，如果以此办法去处理带有副作用（连带影响）的函数，会有一些问题。所以我需要先以 [将查询函数和修改函数分离](making-method-calls-simpler.md#_15) 将函数副作用分离出去。稍后你会看到这方面的例子。


## 以多态取代条件式
---

你手上有个条件式，它根据对象型别的不同而选择不同的行为。

**将这个条件式的每个分支放进一个subclass 内的覆写函数中，然后将原始函数声明为抽象函数（abstract method）。**


```java
double getSpeed() {
    switch (_type) {
    case EUROPEAN:
        return getBaseSpeed();
    case AFRICAN:
        return getBaseSpeed() - getLoadFactor() * _numberOfCoconuts;
    case NORWEGIAN_BLUE:
        return (_isNailed) ? 0 : getBaseSpeed(_voltage);
    }
    throw new RuntimeException ("Should be unreachable");
}
```

![](/images/arrow.gif)

![](/images/09fig01a.gif)

**动机（Motivation）**

在面向对象术语中，听上去最高贵的词非「多态」莫属。多态（polymorphism）最根本的好处就是：如果你需要根据对象的不同型别而采取不同的行为，多态使你不必编写明显的条件式（explicit conditional ）。

正因为有了多态，所以你会发现：「针对type code（型别码）而写的switch 语句」 以及「针对type string （型别名称字符串）而写的if-then-else 语句」在面向对象程序中很少出现。

多态（polymorphism）能够给你带来很多好处。如果同一组条件式在程序许多地点出现，那么使用多态的收益是最大的。使用条件式时，如果你想添加一种新型别，就必须查找并更新所有条件式。但如果改用多态，只需建立一个新的subclass ，并在其中提供适当的函数就行了。class 用户不需要了解这个subclass ，这就大大降低了系统各部分之间的相依程度，使系统升级更加容易。

**作法（Mechanics）**

使用[以多态取代条件式](simplifying-conditional-expressions.md#_6)之前，你首先必须有一个继承结构。你可能已经通过先前的重构得到了这一结构。如果还没有，现在就需要建立它。

要建立继承结构，你有两种选择： [以子类取代型别码](organizing-data.md#_14) 和 [以State/Strategy取代型别码](organizing-data.md#statestrategy)。前一种作法比较简单，因此你应该尽可能使用它。但如果你需要在对象创建好之后修改type code；就不能使用subclassing 作法，只能使用State/Strategy 模式。此，如果由于其他原因你要重构的class 已经有了subclass ，那么也得使用State/Strategy 。记住，如果若干switch 语句针对的是同一个type code；你只需针对这个type code 建立一个继承结构就行 了。

现在，可以向条件式开战了。你的目标可能是switch（case）语句，也可能是if 语句。

- 如果要处理的条件式是一个更大函数中的一部分，首先对条件式进行分析，然后使用[提炼函数](composing-methods.md#_1) 将它提炼到一个独立函数去。
- 如果有必要，使用[搬移函数](moving-features-between-objects.md#_3) 将条件式放置到继承结构的顶端。
- 任选一个subclass ，在其中建立一个函数，使之覆写superclass 中容纳条件式的那个函数。将「与subclass 相关的条件式分支」拷贝到新建函数中，并对它进行适当调整。
    - 为了顺利进行这一步骤，你可能需要将superclass 中的某些private 值域声明为protected 。
- 编译，测试。
- 在superclass 中删掉条件式内被拷贝出去的分支。
- 编译，测试。
- 针对条件式的每个分支，重复上述过程，直到所有分支都被移到subclass 内的函数为止。
- 将superclass 之中容纳条件式的函数声明为抽象函数（abstract method）。


**范例：（Example）**

请允许我继续使用「员工与薪资」这个简单而又乏味的例子。我的classes是从[以State/Strategy取代型别码](organizing-data.md#statestrategy) 那个例子中拿来的，因此示意图就如图9.1所示（如果想知道这个图是怎么得到的，请看第8章范例）。


![](/images/09fig01.gif)

图9.1  继承机构


```java
class Employee...
    int payAmount() {
        switch (getType()) {
        case EmployeeType.ENGINEER:
            return _monthlySalary;
        case EmployeeType.SALESMAN:
            return _monthlySalary + _commission;
        case EmployeeType.MANAGER:
            return _monthlySalary + _bonus;
        default:
            throw new RuntimeException("Incorrect Employee");
        }
    }
    int getType() {
        return _type.getTypeCode();
    }
    private EmployeeType _type;

    abstract class EmployeeType...
    abstract int getTypeCode();

class Engineer extends EmployeeType...
    int getTypeCode() {
        return Employee.ENGINEER;
    }

... and other subclasses
```


switch 语句已经被很好地提炼出来，因此我不必费劲再做一遍。不过我需要将它移至EmployeeType class，因为EmployeeType 才是被subclassing 的class 。

```java
class EmployeeType...
    int payAmount(Employee emp) {
        switch (getTypeCode()) {
            case ENGINEER:
                return emp.getMonthlySalary();
            case SALESMAN:
                return emp.getMonthlySalary() + emp.getCommission();
            case MANAGER:
                return emp.getMonthlySalary() + emp.getBonus();
            default:
                throw new RuntimeException("Incorrect Employee");
        }
    }
```


由于我需要EmployeeType class 的数据，所以我需要将Employee 对象作为参数传递给payAmount()。这些数据中的一部分也许可以移到EmployeeType class 来，但那是另一项重构需要关心的问题了。


调整代码，使之通过编译，然后我修改Employee 中的payAmount() 函数，令它委托（delegate，转调用）EmployeeType ：

```java
class Employee...
    int payAmount() {
        return _type.payAmount(this);
    }
```


现在，我可以处理switch 语句了。这个过程有点像淘气小男孩折磨一只昆虫——每次掰掉它一条腿 6。首先我把switch 语句中的"Engineer"这一分支拷贝到Engineer class：

```java
class Engineer...
    int payAmount(Employee emp) {
        return emp.getMonthlySalary();
    }
```


6译注：「腿」和条件式「分支」的英文都是"leg"。作者幽默地说「掰掉一条腿」， 意思就是「去掉一个分支」。


这个新函数覆写了superclass 中的switch 语句之内那个专门处理"Engineer"的分支。我是个徧执狂，有时我会故意在case 子句中放一个陷阱，检查Engineer class 是否正常工作（是否被调用）：

```java
class EmployeeType...
    int payAmount(Employee emp) {
        switch (getTypeCode()) {
        case ENGINEER:
            throw new RuntimeException ("Should be being overridden");
        case SALESMAN:
            return emp.getMonthlySalary() + emp.getCommission();
        case MANAGER:
            return emp.getMonthlySalary() + emp.getBonus();
        default:
            throw new RuntimeException("Incorrect Employee");
    }
}
```


接下来，我重复上述过程，直到所有分支都被去除为止：

```java
class Salesman...
    int payAmount(Employee emp) {
        return emp.getMonthlySalary() + emp.getCommission();
    }

class Manager...
    int payAmount(Employee emp) {
        return emp.getMonthlySalary() + emp.getBonus();
    }
```


然后，将superclass 的payAmount() 函数声明为抽象函数：

```java
class EmployeeType...
    abstract int payAmount(Employee emp);
```


## 以卫语句取代嵌套条件式
---
 
函数中的条件逻辑（conditional logic）使人难以看清正常的执行路径。
**使用卫语句（guard clauses）表现所有特殊情况。**

```java
double getPayAmount() {
    double result;
    if (_isDead) result = deadAmount();
    else {
        if (_isSeparated) result = separatedAmount();
        else {
            if (_isRetired) result = retiredAmount();
            else result = normalPayAmount();
        }
    }
    return result;
}
```

![](/images/arrow.gif)

```java
double getPayAmount() {
    if (_isDead) return deadAmount();
    if (_isSeparated) return separatedAmount();
    if (_isRetired) return retiredAmount();
    return normalPayAmount();
}
```

**动机（Motivation）**

根据我的经验，条件式通常有两种呈现形式。第一种形式是：所有分支都属于正常行为。第二种形式则是：条件式提供的答案中只有一种是正常行为，其他都是不常见的情况。

这两类条件式有不同的用途，这一点应该通过代码表现出来。如果两条分支都是正常行为，就应该使用形如「if…then…」的条件式；如果某个条件极其罕见，就应该单独检查该条件，并在该条件为真时立刻从函数中返回。这样的单独检查常常被称为「卫语句（guard clauses）」[Beck]。

[以卫语句取代嵌套条件式](simplifying-conditional-expressions.md#_7) 的精髓就是：给某一条分支以特别的重视。如果使用if-then-else 结构，你对if 分支和else 分支的重视是同等的。 这样的代码结构传递给阅读者的消息就是：各个分支有同样的重要性。卫语句（guard clauses）就不同了，它告诉阅读者：『这种情况很罕见，如果它真的发生了，请做 一些必要的整理工作，然后退出。』

「每个函数只能有一个入口和一个出口」的观念，根深蒂固于某些程序员的脑海里。 我发现，当我处理他们编写的代码时，我经常需要使用[以卫语句取代嵌套条件式](simplifying-conditional-expressions.md#_7)。现今的编程语言都会强制保证每个函数只有一个入口， 至于「单一出口」规则，其实不是那么有用。在我看来，保持代码清晰才是最关键的：如果「单一出口」能使这个函数更清楚易读，那么就使用单一出口；否则就不必这么做。

**作法（Mechanics）**

- 对于每个检查，放进一个卫语句（guard clauses）。
    - 卫语句要不就从函数中返回，要不就抛出一个异常（exception）。
- 每次将「条件检查」替换成「卫语句」后，编译并测试。
    - 如果所有卫语句都导致相同结果，请使用[合并条件式](simplifying-conditional-expressions.md#_1)s。


**范例：（Example）**

想像一个薪资系统，其中以特殊规则处理死亡员工、驻外员工、退休员工的薪资。这些情况不常有，但的确偶而会出现。

假设我在这个系统中看到下列代码：

```java
double getPayAmount() {
    double result;
    if (_isDead) result = deadAmount();
    else {
        if (_isSeparated) result = separatedAmount();
        else {
            if (_isRetired) result = retiredAmount();
            else result = normalPayAmount();
        }
    }
    return result;
}
```


在这段代码中，非正常情况的检查掩盖了正常情况的检查，所以我应该使用『卫语句」来取代这些检查，以提高程序清晰度。我可以逐一引入卫语句。让我们从最上面的条件检查动作开始：
```java
double getPayAmount() {
    double result;
    if (_isDead) return deadAmount();
    if (_isSeparated) result = separatedAmount();
    else {
        if (_isRetired) result = retiredAmount();
        else result = normalPayAmount();
    }
    return result;
 }
```


然后，继续下去，仍然一次替换一个检查动作：

```java
double getPayAmount() {
    double result;
    if (_isDead) return deadAmount();
    if (_isSeparated) return separatedAmount();
    if (_isRetired) result = retiredAmount();
    else result = normalPayAmount();
    return result;
}
```


然后是最后一个：

```java
double getPayAmount() {
    double result;
    if (_isDead) return deadAmount();
    if (_isSeparated) return separatedAmount();
    if (_isRetired) return retiredAmount();
    result = normalPayAmount();
    return result;
}
```


此时，result 变量已经没有价值了，所以我把它删掉：

```java
double getPayAmount() {
    if (_isDead) return deadAmount();
    if (_isSeparated) return separatedAmount();
    if (_isRetired) return retiredAmount();
    return normalPayAmount();
}
```


嵌套（nested）条件代码往往由那些深信「每个函数只能有一个出口」的程序员写出。我发现那条规则（函数只能有一个出口）实在有点太简单化了。如果对函数剩余部分不再有兴趣，当然应该立刻退出。引导阅读者去看一个没有用的else 区段，只会妨碍他们的理解。

**范例：将条件逆反（Reversing the Conditions）**

审阅本书初稿时，Joshua Kerievsky 指出：你常常可以将条件表达式逆反，从而实现[以卫语句取代嵌套条件式](simplifying-conditional-expressions.md#_7)。为了拯救我可怜的想像力，他还好心帮我想了个例子：

```java
public double getAdjustedCapital() {
    double result = 0.0;
    if (_capital > 0.0) {
        if (_intRate > 0.0 && _duration > 0.0) {
            result = (_income / _duration) * ADJ_FACTOR;
        }
    }
    return result;
}
```


同样地，我逐一进行替换。不过这次在插入卫语句（guard clauses）时，我需要将相应的条件逆反过来：

```java
public double getAdjustedCapital() {
    double result = 0.0;
    if (_capital <= 0.0) return result;
    if (_intRate > 0.0 && _duration > 0.0) {
        result = (_income / _duration) * ADJ_FACTOR;
    }
    return result;
}
```


下一个条件稍微复杂一点，所以我分两步进行逆反。首先加入一个"logical-NOT"操作：

```java
public double getAdjustedCapital() {
    double result = 0.0;
    if (_capital <= 0.0) return result;
    if (!(_intRate > 0.0 && _duration > 0.0)) return result;
    result = (_income / _duration) * ADJ_FACTOR;
    return result;
}
```


但是在这样的条件式中留下一个"logical-NOT"，会把我的脑袋拧成一团乱麻，所以我把它简化成下面这样：

```java
public double getAdjustedCapital() {
    double result = 0.0;
    if (_capital <= 0.0) return result;
    if (_intRate <= 0.0 || _duration <= 0.0) return result;
    result = (_income / _duration) * ADJ_FACTOR;
    return result;
}
```


这时候我比较喜欢在卫语句（guard clause）内返回一个明确值，因为这样我可以一 目了然地看到卫语句返回的失败结果。此外，这种时候我也会考虑使用[以符号常量/字面常量取代魔法数](organizing-data.md#_10)。

```java
public double getAdjustedCapital() {
    double result = 0.0;
    if (_capital <= 0.0) return 0.0;
    if (_intRate <= 0.0 || _duration <= 0.0) return 0.0;
    result = (_income / _duration) * ADJ_FACTOR;
    return result;
}
```


完成替换之后，我同样可以将临时变量移除：

```java
public double getAdjustedCapital() {
    if (_capital <= 0.0) return 0.0;
    if (_intRate <= 0.0 || _duration <= 0.0) return 0.0;
    return (_income / _duration) * ADJ_FACTOR;
}
```
