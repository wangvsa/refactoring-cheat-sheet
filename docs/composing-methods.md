## 提炼函数
-----------

你有一段代码可以被组织在一起并独立出来。

**将这段代码放进一个独立函数中，并让函数名称解释该函数的用途。**

```java
void printOwing(double amount) {
    printBanner();
    //print details
    System.out.println ("name:" + _name);
    System.out.println ("amount" + amount);
}
```

![](../images/arrow.gif)

```java
void printOwing(double amount) {
    printBanner();
    printDetails(amount);
}
void printDetails (double amount) {
    System.out.println ("name:" + _name);
    System.out.println ("amount" + amount);
}
```

**动机（Motivation）**


[提炼函数](composing-methods.md#_1)是我最常用的重构手法之一。当我看见一个过长的函数或者一段需要注释才能让人理解用途的代码，我就会将这段代码放进一个独立函数中。 

有数个原因造成我喜欢简短而有良好命名的函数。首先，如果每个函数的粒度都很小（finely grained），那么函数之间彼此复用的机会就更大；其次，这会使高层函数码读起来就像一系列注释；再者，如果函数都是细粒度，那么函数的覆写（overridden）也会更容易些。 

的确，如果你习惯看大型函数，恐怕需要一段时间才能适应这种新风格。而且只有当你能给小型函数很好地命名时，它们才能真正起作用，所以你需要在函数名称下点功夫。人们有时会问我，一个函数多长才算合适？在我看来，长度不是问题，关键在于函数名称和函数本体之间的语义距离（semantic distance ）。如果提炼动作 （extracting ）可以强化代码的清晰度，那就去做，就算函数名称比提炼出来的代码 还长也无所谓。 


**作法（Mechanics）**

- 创造一个新函数，根据这个函数的意图来给它命名（以它「做什么」来命名， 而不是以它「怎样做」命名）。
	- 即使你想要提炼（extract）的代码非常简单，例如只是一条消息或一个函数调用，只要新函数的名称能够以更好方式昭示代码意图，你也应该提炼它。但如果你想不出一个更有意义的名称，就别动。
- 将提炼出的代^码从源函数（source）拷贝到新建的目标函数（target）中。
- 仔细检查提炼出的代码，看看其中是否引用了「作用域（scope）限于源函数」的变量（包括局部变量和源函数参数）。
- 检查是否有「仅用于被提炼码」的临时变量（temporary variables ）。如果有，在目标函数中将它们声明为临时变量。 
- 检查被提炼码，看看是否有任何局部变量（local-scope variables ）的值被它改变。如果一个临时变量值被修改了，看看是否可以将被提炼码处理为一个查询（query），并将结果赋值给相关变量。如果很难这样做，或如果被修改的 变量不止一个，你就不能仅仅将这段代码原封不动地离炼出来。你可能需要先使用 [剖解临时变量](composing-methods.md#_6)，然后再尝试提炼。也可以使用[以查询取代临时变量](composing-methods.md#_8)将临时变量消灭掉（请看「范例」中的讨论）。 
- 将被提炼码中需要读取的局部变量，当作参数传给目标函数。
- 处理完所有局部变量之后，进行编译。
- 在源函数中，将被提炼码替换为「对目标函数的调用」。
  - 如果你将任何临时变量移到目标函数中，请检查它们原本的声明式是否在被提炼码的外围。如果是，现在你可以删除这些声明式了。
- 编译，测试。

**范例（examples）：无局部变量（No Local Variables）**

在最简单的情况下，[提炼函数](composing-methods.md#_1) 易如反掌。请看下列函数：
```java
void printOwing() {
    Enumeration e = _orders.elements();
    double outstanding = 0.0;
    // print banner
    System.out.println ("**************************");
    System.out.println ("***** Customer Owes ******");
    System.out.println ("**************************");

    // calculate outstanding
    while (e.hasMoreElements()) {
        Order each = (Order) e.nextElement();
        outstanding += each.getAmount();
    }

    //print details
    System.out.println ("name:" + _name);
    System.out.println ("amount" + outstanding);
}
```

我们可以轻松提炼出「打印banner」的代码。我只需要剪切、粘贴、再插入一个函数调用动作就行了： 

```java
void printOwing() {

    Enumeration e = _orders.elements();
    double outstanding = 0.0;

    printBanner();

    // calculate outstanding
    while (e.hasMoreElements()) {
    Order each = (Order) e.nextElement();
    outstanding += each.getAmount();
}

    //print details
    System.out.println ("name:" + _name);
    System.out.println ("amount" + outstanding);
}

void printBanner() {
    // print banner
    System.out.println ("**************************");
    System.out.println ("***** Customer Owes ******");
    System.out.println ("**************************");
}
```

**范例（Examples）：有局部变量（Using Local Variables）**

果真这么简单，这个重构手法的困难点在哪里？是的，就在局部变量，包括传进源函数的参数和源函数所声明的临时变量。局部变量的作用域仅限于源函数，所以当我使用[提炼函数](composing-methods.md#_1) 时，必须花费额外功夫去处理这些变量。某些时候它们甚至可能妨碍我，使我根本无法进行这项重构。 

局部变量最简单的情况是：被提炼码只是读取这些变量的值，并不修改它们。这种情况下我可以简单地将它们当作参数传给目标函数。所以如果我面对下列函数： 
```java
void printOwing() {
    Enumeration e = _orders.elements();
    double outstanding = 0.0;

    printBanner();

    // calculate outstanding
    while (e.hasMoreElements()) {
        Order each = (Order) e.nextElement();
        outstanding += each.getAmount();
    }

    //print details
    System.out.println ("name:" + _name);
    System.out.println ("amount" + outstanding);
}
```

我就可以将「打印详细信息」这一部分提炼为「带一个参数的函数」：
```java
void printOwing() {
    Enumeration e = _orders.elements();
    double outstanding = 0.0;

    printBanner();

    // calculate outstanding
    while (e.hasMoreElements()) {
        Order each = (Order) e.nextElement();
        outstanding += each.getAmount();
    }

    printDetails(outstanding);
}

void printDetails (double outstanding) {
    System.out.println ("name:" + _name);
    System.out.println ("amount" + outstanding);
}
```

必要的话，你可以用这种手法处理多个局部变量。

如果局部变量是个对象，而被提炼码调用了会对该对象造成修改的函数，也可以如法炮制。你同样只需将这个对象作为参数传递给目标函数即可。只有在被提炼码真的对一个局部变量赋值的情况下，你才必须采取其他措施。


**范例（Examples）：对局部变量再赋值（Reassigning a Local Variable）**

如果被提炼码对局部变量赋值，问题就变得复杂了。这里我们只讨论临时变量的问题。如果你发现源函数的参数被赋值，应该马上使用[移除对参数的赋值](composing-methods.md#_7)。 

被赋值的临时变量也分两种情况。较简单的情况是：这个变量只在被提炼码区段中使用。果真如此，你可以将这个临时变量的声明式移到被提炼码中，然后一起提炼出去。另一种情况是：被提炼码之外的代码也使用了这个变量。这又分为两种情况： 如果这个变量在被提炼码之后未再被使用，你只需直接在目标函数中修改它就可以了；如果被提炼码之后的代码还使用了这个变量，你就需要让目标函数返回该变量改变后的值。我以下列代码说明这几种不同情况： 
```java
void printOwing() {

    Enumeration e = _orders.elements();
    double outstanding = 0.0;

    printBanner();

    // calculate outstanding
    while (e.hasMoreElements()) {
        Order each = (Order) e.nextElement();
        outstanding += each.getAmount();
    }

    printDetails(outstanding);
}
```

现在我把「计算」代码提炼出来：
```java
void printOwing() {
    printBanner();
    double outstanding = getOutstanding();
    printDetails(outstanding);
}

double getOutstanding() {
    Enumeration e = _orders.elements();
    double outstanding = 0.0;
    while (e.hasMoreElements()) {
        Order each = (Order) e.nextElement();
        outstanding += each.getAmount();
    }
    return outstanding;
}
```

Enumeration变量 e只在被提炼码中用到，所以我可以将它整个搬到新函数中。double变量outstanding在被提炼码内外都被使用到，所以我必须让提炼出来的新函数返回它。编译测试完成后，我就把回传值改名，遵循我的一贯命名原则： 

```java
double getOutstanding() {
    Enumeration e = _orders.elements();
    double result = 0.0;
    while (e.hasMoreElements()) {
        Order each = (Order) e.nextElement();
        result = each.getAmount();
    }
    return result;
}
```

本例中的outstanding变量只是很单纯地被初始化为一个明确初值，所以我可以只在新函数中对它初始化。如果代码还对这个变量做了其他处理，我就必须将它的值作为参数传给目标函数。对于这种变化，最初代码可能是这样： 
```java
void printOwing(double previousAmount) {

    Enumeration e = _orders.elements();
    double outstanding = previousAmount * 1.2;

    printBanner();

    // calculate outstanding
    while (e.hasMoreElements()) {
        Order each = (Order) e.nextElement();
        outstanding += each.getAmount();
    }
    printDetails(outstanding);
}
```


提炼后的代码可能是这样：
```java
void printOwing(double previousAmount) {
    double outstanding = previousAmount * 1.2;
    printBanner();
    outstanding = getOutstanding(outstanding);
    printDetails(outstanding);
}

double getOutstanding(double initialValue) {
    double result = initialValue;
    Enumeration e = _orders.elements();
    while (e.hasMoreElements()) {
        Order each = (Order) e.nextElement();
        result += each.getAmount();
    }
    return result;
}
```


编译并测试后，我再将变量outstanding初始化过程整理一下：
```java
void printOwing(double previousAmount) {
    printBanner();
    double outstanding = getOutstanding(previousAmount * 1.2);
    printDetails(outstanding);
}
```

这时候，你可能会问：『如果需要返回的变量不止一个，又该怎么办呢？』


你有数种选择。最好的选择通常是：挑选另一块代码来提炼。我比较喜欢让每个函 数都只返回一个值，所以我会安排多个函数，用以返回多个值。如果你使用的语言支持「输出式参数」（output parameters），你可以使用它们带回多个回传值。但我还是尽可能选择单一返回值。 

临时变量往往为数众多，甚至会使提炼工作举步维艰。这种情况下，我会尝试先运用 [以查询取代临时变量](composing-methods.md#_8) 减少临时变量。如果即使这么做了提炼依旧困难重重，我就会动用[以函数对象取代函数](composing-methods.md#_9)，这个重构手法不在乎代码中有多少临时变量，也不在乎你如何使用它们。 

## 将函数内联化
---------------

一个函数，其本体（method body）应该与其名称（method name)同样清楚易懂。

**在函数调用点插入函数本体，然后移除该函数。**
```java
int getRating() {
  return (moreThanFiveLateDeliveries()) ? 2 : 1;
}
boolean moreThanFiveLateDeliveries() {
  return _numberOfLateDeliveries > 5;
}
```
![](../images/arrow.gif)
```java
int getRating() {
  return (_numberOfLateDeliveries > 5) ? 2 : 1;
}
```

**动机（Motivation）**

本书经常以简短的函数表现动作意图，这样会使代码更清晰易读。但有时候你会遇到某些函数，其内部代码和函数名称同样清晰易读。也可能你重构了该函数，使得其内容和其名称变得同样清晰。果真如此，你就应该去掉这个函数，直接使用其中的代码。间接性可能带来帮助，但非必要的间接性总是让人不舒服。

另一种需要使用[将函数内联化](composing-methods.md#_2) 的情况是：你手上有一群组织不甚合理的函数。你可以将它们都inline到一个大型函数中，再从中提炼出组织合理的小型函数。Kent Beck发现，实施 [以函数对象取代函数](composing-methods.md#_9) 之前先这么做，往往可以获得不错的效果。你可以把你所要的函数（有着你要的行为）的所有调用对象的函数内容都inline到method object（函数对象）中。比起既要移动一个函数，又要移动它所调用的其他所有函数，「将大型函数作为单一整体来移动」会比较简单。

如果别人使用了太多间接层，使得系统中的所有函数都似乎只是对另一个函数的简单委托（delegation），造成我在这些委托动作之间晕头转向，那么我通常都会使用[将函数内联化](composing-methods.md#_2)。当然，间接层有其价值，但不是所有间接层都有价值。试着使用inlining，我可以找出那些有用的间接层，同时将那些无用的间接层去除。


**作法（Mechanics）**


- 检查函数，确定它不具多态性（is not polymorphic）。
  - 如果subclass继承了这个函数,就不要将此函数inline化，因为subclass无法覆写（overridde）一个根本不存在的函数。
- 找出这个函数的所有被调用点。
- 将这个函数的所有被调用点都替换为函数本体（代码）。
- 编译，测试。
- 删除该函数的定义。

被我这样一写，[将函数内联化](composing-methods.md#_2) 似乎很简单。但情况往往并非如此。对于递归调用、多返回点、inlining至另一个对象中而该对象并无提供访问函数（accessors）……，每一种情况我都可以写上好几页。我之所以不写这些特殊情况， 原因很简单：如果你遇到了这样的复杂情况，那么就不应该使用这个重构手法。
    
## 将临时变量内联化
-------------------


你有一个临时变量，只被一个简单表达式赋值一次，而它妨碍了其他重构手法。
 
**将所有对该变量的引用动作，替换为对它赋值的那个表达式本身。**

```java
  double basePrice = anOrder.basePrice();
  return (basePrice > 1000)
```
![](../images/arrow.gif)

```java
  return (anOrder.basePrice() > 1000)
```


**动机（Motivation）**


[将临时变量内联化](composing-methods.md#_3)多半是作为[以查询取代临时变量](composing-methods.md#_8) 的一部分来使用，所以真正的动机出现在后者那儿。惟一单独使用[将临时变量内联化](composing-methods.md#_3)的情况是：你发现某个临时变量被赋予某个函数调用的返回值。一般来说，这样的临时变量不会有任何危害，你可以放心地把它留在那儿。但如果这个临时变量妨碍了其他的重构 手法——例如[提炼函数](composing-methods.md#_1)，你就应该将它inline化。


**作法（Mechanics）**

- 如果这个临时变量并未被声明为final，那就将它声明为final，然后编译。
- 这可以检查该临时变量是否真的只被赋值一次。
- 找到该临时变量的所有引用点，将它们替换为「为临时变量赋值」之语句中的等号右侧表达式。
- 每次修改后，编译并测试。
- 修改完所有引用点之后，删除该临时变量的声明式和赋值语句。
- 编译，测试。

## 以查询取代临时变量
---------------------


你的程序以一个临时变量（temp）保存某一表达式的运算结果。
 

**将这个表达式提炼到一个独立函数（译注：所谓查询式，query）中。将这个临时变量的所有「被引用点」替换为「对新函数的调用」。新函数可被其他函数使用。**

```java
double basePrice = _quantity * _itemPrice;
if (basePrice > 1000)
    return basePrice * 0.95;
else
    return basePrice * 0.98;
```

![](../images/arrow.gif)

```java
if (basePrice() > 1000)
    return basePrice() * 0.95;
else
    return basePrice() * 0.98;
```
...

```java
double basePrice() {
    return _quantity * _itemPrice;
}
```


**动机（Motivation）**
 
临时变量的问题在于：它们是暂时的，而且只能在所属函数内使用。由于临时变量只有在所属函数内才可见，所以它们会驱使你写出更长的函数，因为只有这样你才能访问到想要访问的临时变量。如果把临时变量替换为一个查询式（query method），那么同一个class中的所有函数都将可以获得这份信息。这将带给你极大帮助，使你能够为这个编写更清晰的代码。

[以查询取代临时变量](composing-methods.md#_8)往往是你运用[提炼函数](composing-methods.md#_1) 之前必不可少的一个步骤。局部变量会使代码难以被提炼，所以你应该尽可能把它们替换为查询式。
 
这个重构手法较为直率的情况就是：临时变量只被赋值一次，或者赋值给临时变量的表达式不受其他条件影响。其他情况比较棘手，但也有可能发生。你可能需要先运用[剖解临时变量](composing-methods.md#_6)或[将查询函数和修改函数分离](making-method-calls-simpler.md#_15)使情况变得简单一些，然后再替换临时变量。如果你想替换的临时变量是用来收集结果的（例如循环中的累加值），你就需要将某些程序逻辑（例如循环）拷贝到查询式（query method）去。
 
**作法（Mechanics）**
 

首先是简单情况：

- 找出只被赋值一次的临时变量。
- 如果某个临时变量被赋值超过一次，考虑使用[剖解临时变量](composing-methods.md#_6) 将它分割成多个变量。
- 将该临时变量声明为final。
- 编译。
- 这可确保该临时变量的确只被赋值一次。
- 将「对该临时变量赋值」之语句的等号右侧部分提炼到一个独立函数中。
  - 首先将函数声明为private。日后你可能会发现有更多class需要使用 它，彼时你可轻易放松对它的保护。
  - 确保提炼出来的函数无任何连带影响（副作用），也就是说该函数并不修改任何对象内容。如果它有连带影响，就对它进行[将查询函数和修改函数分离](making-method-calls-simpler.md#_15)。
- 编译，测试。
- 在该临时变量身上实施[以查询取代临时变量](composing-methods.md#_8)。

我们常常使用临时变量保存循环中的累加信息。在这种情况下，整个循环都可以被提为一个独立函数，这也使原本的函数可以少掉几行扰人的循环码。有时候，你可能会用单一循环累加好几个值，就像本书p.26的例子那样。这种情况下你应该针对每个累加值重复一遍循环，这样就可以将所有临时变量都替换为查询式（query）。当然，循环应该很简单，复制这些代码时才不会带来危险。

运用此手法，你可能会担心性能问题。和其他性能问题一样，我们现在不管它，因 为它十有八九根本不会造成任何影响。如果性能真的出了问题，你也可以在优化时期解决它。如果代码组织良好，那么你往往能够发现更有效的优化方案；如果你没有进行重构，好的优化方案就可能与你失之交臂。如果性能实在太糟糕，要把临时变量放回去也是很容易的。
 
**范例（Example）**

首先，我从一个简单函数开始：

```java
double getPrice() {
    int basePrice = _quantity * _itemPrice;
    double discountFactor;
    if (basePrice > 1000)
        discountFactor = 0.95;
    else
        discountFactor = 0.98;
    return basePrice * discountFactor;
}
```


我希望将两个临时变量都替换掉。当然，每次一个。


尽管这里的代码十分清楚，我还是先把临时变量声明为final，检查他们是否的确只被赋值一次：

```java
double getPrice() {
    final int basePrice = _quantity * _itemPrice;
    final double discountFactor;
    if (basePrice > 1000)
        discountFactor = 0.95;
    else
        discountFactor = 0.98;
    return basePrice * discountFactor;
}
```


这样一来，如果有任何问题，编译器就会警告我。之所以先做这件事，因为如果临时变量不只被赋值一次，我就不该进行该项重构。接下来我开始替换临时变量，每次一个。首先我把赋值（assignment）动作的右侧表达式提炼出来：

```java
double getPrice() {
    final int basePrice = basePrice();
    final double discountFactor;
    if (basePrice > 1000) discountFactor = 0.95;
    else discountFactor = 0.98;
    return basePrice * discountFactor;
}

private int basePrice() {
    return _quantity * _itemPrice;
}
```


编译并测试，然后开始使用[以查询取代临时变量](composing-methods.md#_8)。首先把临时变量basePrice的第一个引用点替换掉：

```java
double getPrice() {
    final int basePrice = basePrice();
    final double discountFactor;
    if (basePrice() > 1000) discountFactor = 0.95;
    else discountFactor = 0.98;
    return basePrice * discountFactor;
}
```


编译、测试、下一个（听起来像在指挥人们跳乡村舞蹈一样）。由于「下一个」已经是basePrice的最后一个引用点，所以我把basePrice临时变量的声明式一并摘除：

```java
double getPrice() {
    final double discountFactor;
    if (basePrice() > 1000) discountFactor = 0.95;
    else discountFactor = 0.98;
    return basePrice() * discountFactor;
}
```


搞定basePrice之后，我再以类似办法提炼出一个discountFactor()：

```java
double getPrice() {
    final double discountFactor = discountFactor();
    return basePrice() * discountFactor;
}

private double discountFactor() {
    if (basePrice() > 1000) return 0.95;
    else return 0.98;
}
```


你看，如果我没有把临时变量basePrice替换为一个查询式，将多么难以提炼discountFactor()！

最终，getPrice()变成了这样：

```java
double getPrice() {
    return basePrice() * discountFactor();
}
```

## 引入解释性变量
-----------------

你有一个复杂的表达式。

**将该表达式（或其中一部分）的结果放进一个临时变量，以此变量名称来解释表达式用途。**

```java
if ( (platform.toUpperCase().indexOf("MAC") > -1) && (browser.toUpperCase().indexOf("IE") > -1) &&
    wasInitialized() && resize > 0 ) {
    // do something
}
```

![](../images/arrow.gif)

```java
final boolean isMacOs     = platform.toUpperCase().indexOf("MAC") > -1;
final boolean isIEBrowser = browser.toUpperCase().indexOf("IE")  > -1;
final boolean wasResized  = resize > 0;

if (isMacOs && isIEBrowser && wasInitialized() && wasResized) {
    // do something
}
```


**动机（Motivation）**
 
表达式有可能非常复杂而难以阅读。这种情况下，临时变量可以帮助你将表达式分解为比较容易管理的形式。

在条件逻辑（conditional logic ）中，[引入解释性变量](composing-methods.md#_5)特别有价值：你可以用这项重构将每个条件子句提炼出来，以一个良好命名的临时变量来解释对应条件子句的意义。使用这项重构的另一种情况是，在较长算法中，可以运用临时变量来解释每一步运算的意义。

[引入解释性变量](composing-methods.md#_5)是一个很常见的重构手法，但我得承认，我并不常用它。我几乎总是尽量使用 [提炼函数](composing-methods.md#_1) 来解释一段代码的意义。毕竟临时变量只在它所处的那个函数中才有意义，局限性较大，函数则可以在对象的整个生命中都有用，并且可被其他对象使用。但有时候，当局部变量使 [提炼函数](composing-methods.md#_1) 难以进行时，我就使用[引入解释性变量](composing-methods.md#_5)。


**作法（Mechanics）**


- 声明一个final临时变量，将待分解之复杂表达式中的一部分动作的运算结果赋值给它。
- 将表达式中的「运算结果」这一部分，替换为上述临时变量。
	- 如果被替换的这一部分在代码中重复出现，你可以每次一个，逐一替换。
- 编译，测试。
- 重复上述过程，处理表达式的其他部分。



**范例（Example）**

我们从一个简单计算开始：
``java
double price() {
    // price is base price - quantity discount + shipping
    return _quantity * _itemPrice -
    Math.max(0, _quantity - 500) * _itemPrice * 0.05 +
    Math.min(_quantity * _itemPrice * 0.1, 100.0);
}
```

这段代码还算简单，不过我可以让它变得更容易理解。首先我发现，底价（base price）等于数量（quantity）乘以单价（item price）。于是我把这一部分计算的结果放进 一个临时变量中：

```java
double price() {
    // price is base price - quantity discount + shipping
    final double basePrice = _quantity * _itemPrice;
    return basePrice -
    Math.max(0, _quantity - 500) * _itemPrice * 0.05 +
    Math.min(_quantity * _itemPrice * 0.1, 100.0);
}
```

稍后也用上了「数量乘以单价」运算结果，所以我同样将它替换为basePrice临时变量：

```java
double price() {
    // price is base price - quantity discount + shipping
    final double basePrice = _quantity * _itemPrice;
    return basePrice -
    Math.max(0, _quantity - 500) * _itemPrice * 0.05 +
    Math.min(basePrice * 0.1, 100.0);
}
```

然后，我将批发折扣（quantity discount）的计算提炼出来，将结果赋予临时变量 quantityDiscount：
```java
double price() {
    // price is base price - quantity discount + shipping
    final double basePrice = _quantity * _itemPrice;
    final double quantityDiscount = Math.max(0, _quantity - 500) * _itemPrice * 0.05;
    return basePrice - quantityDiscount +
    Math.min(basePrice * 0.1, 100.0);
}
```

最后，我再把运费（shipping）计算提炼出来，将运算结果赋予临时变量shipping。 同时我还可以删掉代码中的注释，因为现在代码已经可以完美表达自己的意义了：
```java
double price() {
    final double basePrice = _quantity * _itemPrice;
    final double quantityDiscount = Math.max(0, _quantity - 500) * _itemPrice * 0.05;
    final double shipping = Math.min(basePrice * 0.1, 100.0);
    return basePrice - quantityDiscount + shipping;
}
```


**运用 [提炼函数](composing-methods.md#_1)处理上述范例**

面对上述代码，我通常不会以临时变量来解释其动作意图，我更喜欢使用 [提炼函数](composing-methods.md#_1)。让我们回到起点：

```java
double price() {
    // price is base price - quantity discount + shipping
    return _quantity * _itemPrice -
    Math.max(0, _quantity - 500) * _itemPrice * 0.05 +
    Math.min(_quantity * _itemPrice * 0.1, 100.0);
}
```

这一次我把底价计算提炼到一个独立函数中：

```java
double price() {
// price is base price - quantity discount + shipping
return basePrice() -
    Math.max(0, _quantity - 500) * _itemPrice * 0.05 +
    Math.min(basePrice() * 0.1, 100.0);
}

private double basePrice() {
    return _quantity * _itemPrice;
}
```

我继续我的提炼，每次提炼出一个新函数。最后得到下列代码：

```java
double price() {
    return basePrice() - quantityDiscount() + shipping();
}

private double quantityDiscount() {
    return Math.max(0, _quantity - 500) * _itemPrice * 0.05;
}

private double shipping() {
    return Math.min(basePrice() * 0.1, 100.0);
}

private double basePrice() {
    return _quantity * _itemPrice;
}
```

我比较喜欢使用 [提炼函数](composing-methods.md#_1)，因为同一对象中的任何部分，都可以根据自己的需要去取用这些提炼出来的函数。一开始我会把这些新函数声明为private； 如果其他对象也需要它们，我可以轻易释放这些函数的访问限制。我还发现， [提炼函数](composing-methods.md#_1)的工作量通常并不比[引入解释性变量](composing-methods.md#_5) 来得大。

那么，应该在什么时候使用[引入解释性变量](composing-methods.md#_5) 呢？答案是：在 [提炼函数](composing-methods.md#_1) 需要花费更大工作量时。如果我要处理的是一个拥有大量局部变量的算法，那么使用 [提炼函数](composing-methods.md#_1) 绝非易事。这种情况下我会使用[引入解释性变量](composing-methods.md#_5) 帮助我理清代码，然后再考虑下一步该怎么办。搞清楚代码逻辑之后，我总是可以运用 [以查询取代临时变量](composing-methods.md#_8) 把被我引入的那些解释性临时变量去掉。况且，如果我最终使用[以函数对象取代函数](composing-methods.md#_9)，那么被我引入的那些解释性临时变量也有其价值。

## 剖解临时变量
---------------

你的程序有某个临时变量被赋值超过一次，它既不是循环变量，也不是一个集用临时变量（collecting temporary variable）。
 
**针对每次赋值，创造一个独立的、对应的临时变量。**

```java
double temp = 2 * (_height + _width);
System.out.println (temp);
temp = _height * _width;
System.out.println (temp);
```

![](../images/arrow.gif)

```java
final double perimeter = 2 * (_height + _width);
System.out.println (perimeter);
final double area = _height * _width;
System.out.println (area);
```

 
**动机（Motivation）**
 
临时变量有各种不同用途，其中某些用途会很自然地导致临时变量被多次赋值。「循环变量」和「集用临时变量」就是两个典型例子：循环变量（loop variables ）[Beck]会随循环的每次运行而改变〔例如for (int i=0; i<10; i++)语句中的i〕；集用临时变量（collecting temporary variable）[Beck]负责将「通过整个函数的运算」而构成的某个值收集起来。
 
除了这两种情况，还有很多临时变量用于保存一段冗长代码的运算结果，以便稍后使用。这种临时变量应该只被赋值一次。如果它们被赋值超过一次，就意味它们在函数中承担了一个以上的责任。如果临时变量承担多个责任，它就应该被替换（剖 解）为多个临时变量，每个变量只承担一个责任。同一个临时变量承担两件不同的 事情，会令代码阅读者糊涂。

 
**作法（Mechanics）**
 
- 在「待剖解」之临时变量的声明式及其第一次被赋值处，修改其名称。
	
- 如果稍后之赋值语句是「i = i +某表达式」形式，就意味这是个集用临时变量，那么就不要剖解它。集用临时变量的作用通常是累加、字符串接合、写入stream或者向群集（collection）添加元素。
	
- 将新的临时变量声明为final。
 
- 以该临时变量之第二次赋值动作为界，修改此前对该临时变量的所有引用点，让它们引用新的临时变量。
 
- 在第二次赋值处，重新声明原先那个临时变量。
 
- 编译，测试。
 
- 逐次重复上述过程。每次都在声明处对临时变量易名，并修改下次赋值之前的引用点。
 


**范例（Example）**

下面范例中我要计算一个苏格兰布丁（haggis）运动的距离。在起点处，静止的苏格兰布丁会受到一个初始力的作用而开始运动。一段时间后，第二个力作用于布丁，让它再次加速。根据牛顿第二定律，我可以这样计算布丁运动的距离：

```java
double getDistanceTravelled (int time) {
    double result;
    double acc = _primaryForce / _mass;        //译注：第一次赋值处
    int primaryTime = Math.min(time, _delay);
    result = 0.5 * acc * primaryTime * primaryTime;
    int secondaryTime = time - _delay;
    if (secondaryTime > 0) {
        double primaryVel = acc * _delay;        //以下是第二次赋值处
        acc = (_primaryForce + _secondaryForce) / _mass;        
        result +=  primaryVel * secondaryTime + 0.5 * acc * secondaryTime * secondaryTime;
    }
    return result;
}
```


真是个绝佳的丑陋小东西。注意观察此例中的acc变量如何被赋值两次。acc变量有两个责任：第一是保存第一个力造成的初始加速度；第二是保存两个力共同造成的加速度。这就是我想要剖解的东西。

首先，我在函数开始处修改这个临时变量的名称，并将新的临时变量声明为final。 接下来我把第二次赋值之前对acc变量的所有引用点，全部改用新的临时变量。最后，我在第二次赋值处重新声明acc变量：

```java
double getDistanceTravelled (int time) {
    double result;
    final   double primaryAcc  = _primaryForce / _mass;
    int primaryTime = Math.min(time, _delay);
    result = 0.5 * primaryAcc * primaryTime * primaryTime;
    int secondaryTime = time - _delay;
    if (secondaryTime > 0) {
        double primaryVel = primaryAcc * _delay;
        double acc = (_primaryForce + _secondaryForce) / _mass;
        result +=  primaryVel * secondaryTime + 0.5 * acc * secondaryTime * secondaryTime;
    }
    return result;
}
```


新的临时变量的名称指出，它只承担原先acc变量的第一个责任。我将它声明为final，确保它只被赋值一次。然后，我在原先变量第二次被赋值处重新声明acc。现在，重新编译并测试，一切都应该没有问题。

然后，我继续处理临时变量的第二次赋值。这次我把原先的临时变量完全删掉，代之以一个新的临时变量。新变量的名称指出，它只承担原先变量的第二个责任：

```java
double getDistanceTravelled (int time) {
    double result;
    final double primaryAcc = _primaryForce / _mass;
    int primaryTime = Math.min(time, _delay);
    result = 0.5 * primaryAcc * primaryTime * primaryTime;
    int secondaryTime = time - _delay;
    if (secondaryTime > 0) {
        double primaryVel = primaryAcc * _delay;
        final double secondaryAcc = (_primaryForce + _secondaryForce) / _mass;
        result +=  primaryVel * secondaryTime + 0.5 *
        secondaryAcc * secondaryTime * secondaryTime;
    }
    return result;
}
```
 
现在，这段代码肯定可以让你想起更多其他重构手法。尽情享受吧。（我敢保证， 这比吃苏格兰布丁强多了 ——你知道他们都在里面放了些什么东西吗？<sup>4</sup>）
 
<i>
<sup>4</sup>译注：苏格兰布丁（haggis）是一种苏格兰菜，把羊心等内脏装在羊胃里煮成。由于它被羊胃包成一个球体，因此可以像球一样踢来踢去，这就是本例的由来。「把羊心装在羊胃里煮成…」，呃，有些人难免对这道菜恶心，Martin Fowler想必是其中之一。
</i>
 
## 移除对参数的赋值
-------------------

你的代码对一个参数进行赋值动作。

**以一个临时变量取代该参数的位置。**
```java
int discount (int inputVal, int quantity, int yearToDate) {
    if (inputVal > 50) inputVal -= 2;
```
![](../images/arrow.gif)

```java
int discount (int inputVal, int quantity, int yearToDate) {
    int result = inputVal;
    if (inputVal > 50) result -= 2;
``` 


**动机（Motivation）**

首先，我要确定大家都清楚「对参数赋值」这个说法的意思。如果你把一个名为foo 的对象作为参数传给某个函数，那么「对参数赋值」意味改变foo，使它引用（参考、指涉、指向）另一个对象。如果你在「被传入对象」身上进行什么操作，那没问题，我也总是这样干。我只针对「foo被改而指向（引用）完全不同的另一个对象」这种情况来讨论：

```java
void aMethod(Object foo) {
    foo.modifyInSomeWay();           // that's OK
    foo = anotherObject;             // trouble and despair will follow you
```
 
我之所以不喜欢这样的作法，因为它降低了代码的清晰度，而且混淆了 pass by value（传值〕和 pass by reference (传址）这两种参数传递方式。Java只采用 pass by value传递方式（稍后讨论），我们的讨论也正是基于这一点。
 
在 pass by value情况下，对参数的任何修改，都不会对调用端造成任何影响。那些用过 pass by reference的人可能会在这一点上犯糊涂。
 
另一个让人糊涂的地方是函数本体内。如果你只以参数表示「被传递进来的东西」，那么代码会清晰得多，因为这种用法在所有语言中都表现出相同语义。
 
在Java中，不要对参数赋值；如果你看到手上的代码已经这样做了，请使用[移除对参数的赋值](composing-methods.md#_7)。

当然，面对那些使用「输出式参数」（ output parameters）的语言，你不必遵循这条规则。不过在那些语言中我会尽量少用输出式参数。
 

**作法（Mechanics）**
 
- 建立一个临时变量，把待处理的参数值赋予它。
 
- 以「对参数的赋值动作」为界，将其后所有对此参数的引用点，全部替换为「对此临时变量的引用动作」。
 
- 修改赋值语句，使其改为对新建之临时变量赋值。
 
- 编译，测试。

- 如果代码的语义是 pass by reference，请在调用端检查调用后是否还使用了这个参数。也要检查有多少个 pass by reference参数「被赋值后又被使用」。请尽量只以return方式返回一个值。如果需要返回的值不只一个，看看可否把需返回的大堆数据变成单一对象，或千脆为每个返回值设计对应的一个独立函数。
 


**范例（Example）**
 
我从下列这段简单代码开始：
```java
int discount (int inputVal, int quantity, int yearToDate) {
    if (inputVal > 50) inputVal -= 2;
    if (quantity > 100) inputVal -= 1;
    if (yearToDate > 10000) inputVal -= 4;
    return inputVal;
}
```

以临时变量取代对参数的赋值动作，得到下列代码：
```java 
int discount (int inputVal, int quantity, int yearToDate) {
    int result = inputVal;
    if (inputVal > 50) result -= 2;
    if (quantity > 100) result -= 1;
    if (yearToDate > 10000) result -= 4;
    return result;
}
```

还可以为参数加上关键词final，从而强制它遵循「不对参数赋值」这一惯例：
```java
int discount (final int inputVal, final int quantity, final int yearToDate) {
    int result = inputVal;
    if (inputVal > 50) result -= 2;
    if (quantity > 100) result -= 1;
    if (yearToDate > 10000) result -= 4;
    return result;
}
```

不过我得承认，我并不经常使用final来修饰参数，因为我发现，对于提高短函数的清晰度，这个办法并无太大帮助。我通常会在较长的函数中使用它，让它帮助我检查参数是否被做了修改。

 

**Java 的 pass by value（传值）**
 
Java使用"pass by value"「函数调用」方式，这常常造成许多人迷惑。在所有地点，Java都严格釆用pass by value，所以下列程序：
```java
class Param {
    public static void main(String[] args) {
        int x = 5;
        triple(x);
        System.out.println ("x after triple: " + x);
    }
    private static void triple(int arg) {
        arg = arg * 3;
        System.out.println ("arg in triple: " + arg);
    }
}
```

 
会产生这样的输出：

```java 
arg in triple: 15
x after triple: 5
``` 


这段代码还不至于让人糊涂。但如果参数中传递的是对象，就可能把人弄迷糊了。如果我在程序中以Date对象表示日期，那么下列程序：

```java 
class Param {
 
    public static void main(String[] args) {
        Date d1 = new Date ("1 Apr 98");
        nextDateUpdate(d1);
        System.out.println ("d1 after nextDay: " + d1);
 
        Date d2 = new Date ("1 Apr 98");
        nextDateReplace(d2);
        System.out.println ("d2 after nextDay: " + d2);
    }
 
    private static void nextDateUpdate (Date arg) {
        arg.setDate(arg.getDate() + 1);
        System.out.println ("arg in nextDay: " + arg);
    }
 
    private static void nextDateReplace (Date arg) {
        arg = new Date (arg.getYear(), arg.getMonth(), arg.getDate() + 1);
        System.out.println ("arg in nextDay: " + arg);
    }
}
``` 


产生的输出是：

```java 
arg in nextDay: Thu Apr 02 00:00:00 EST 1998
d1 after nextDay: Thu Apr 02 00:00:00 EST 1998
arg in nextDay: Thu Apr 02 00:00:00 EST 1998
d2 after nextDay: Wed Apr 01 00:00:00 EST 1998
```
 
从本质上说，object reference是按值传递的（passed by value）。因此我可以修改参数对象的内部状态，但对参数对象重新赋值，没有意义。

Java1.1及其后版本，允许你将参数标示为final，从而避免函数中对参数赋值。 即使某个参数被标示为final，你仍然可以修改它所指向的对象。我总是把参数视为final，但是我得承认，我很少在参数列（parameter list）中这样标示它们。

## 以查询取代临时变量
---------------------

你的程序以一个临时变量（temp）保存某一表达式的运算结果。

**将这个表达式提炼到一个独立函数（译注：所谓查询式，query）中。将这个临时变量的所有「被引用点」替换为「对新函数的调用」。新函数可被其他函数使用。**

```java
    double basePrice = _quantity * _itemPrice;
    if (basePrice > 1000)
        return basePrice * 0.95;
    else
        return basePrice * 0.98;
```

![](../images/arrow.gif)

```java
    if (basePrice() > 1000)
        return basePrice() * 0.95;
    else
        return basePrice() * 0.98;
```

...

```java
  double basePrice() {
      return _quantity * _itemPrice;
  }
```


**动机（Motivation）**
 

临时变量的问题在于：它们是暂时的，而且只能在所属函数内使用。由于临时变量只有在所属函数内才可见，所以它们会驱使你写出更长的函数，因为只有这样你才能访问到想要访问的临时变量。如果把临时变量替换为一个查询式（query method），那么同一个class中的所有函数都将可以获得这份信息。这将带给你极大帮助，使你能够为这个编写更清晰的代码。
 

[以查询取代临时变量](composing-methods.md#_8)往往是你运用[提炼函数](composing-methods.md#_1) 之前必不可少的一个步骤。局部变量会使代码难以被提炼，所以你应该尽可能把它们替换为查询式。
 

这个重构手法较为直率的情况就是：临时变量只被赋值一次，或者赋值给临时变量的表达式不受其他条件影响。其他情况比较棘手，但也有可能发生。你可能需要先运用 [剖解临时变量](composing-methods.md#_6) 或[将查询函数和修改函数分离](making-method-calls-simpler.md#_15) 使情况变得简单一些，然后再替换临时变量。如果你想替换的临时变量是用来收集结果的（例如循环中的累加值），你就需要将某些程序逻辑（例如循环）拷贝到查询式（query method）去。

 
**作法（Mechanics）**
 

首先是简单情况：

- 找出只被赋值一次的临时变量。
- 如果某个临时变量被赋值超过一次，考虑使用[剖解临时变量](composing-methods.md#_6) 将它分割成多个变量。
- 将该临时变量声明为final。
- 编译。
- 这可确保该临时变量的确只被赋值一次。
- 将「对该临时变量赋值」之语句的等号右侧部分提炼到一个独立函数中。
  
  - 首先将函数声明为private。日后你可能会发现有更多class需要使用 它，彼时你可轻易放松对它的保护。
  - 确保提炼出来的函数无任何连带影响（副作用），也就是说该函数并不修改任何对象内容。如果它有连带影响，就对它进行[将查询函数和修改函数分离](making-method-calls-simpler.md#_15)。
  
- 编译，测试。
- 在该临时变量身上实施[以查询取代临时变量](composing-methods.md#_8)。



我们常常使用临时变量保存循环中的累加信息。在这种情况下，整个循环都可以被提为一个独立函数，这也使原本的函数可以少掉几行扰人的循环码。有时候，你可能会用单一循环累加好几个值，就像本书p.26的例子那样。这种情况下你应该针对每个累加值重复一遍循环，这样就可以将所有临时变量都替换为查询式（query）。当然，循环应该很简单，复制这些代码时才不会带来危险。
 

运用此手法，你可能会担心性能问题。和其他性能问题一样，我们现在不管它，因 为它十有八九根本不会造成任何影响。如果性能真的出了问题，你也可以在优化时期解决它。如果代码组织良好，那么你往往能够发现更有效的优化方案；如果你没有进行重构，好的优化方案就可能与你失之交臂。如果性能实在太糟糕，要把临时变量放回去也是很容易的。

 
**范例（Example）**



首先，我从一个简单函数开始：

```java
double getPrice() {
    int basePrice = _quantity * _itemPrice;
    double discountFactor;
    if (basePrice > 1000) discountFactor = 0.95;
    else discountFactor = 0.98;
    return basePrice * discountFactor;
} 
```


我希望将两个临时变量都替换掉。当然，每次一个。
 

尽管这里的代码十分清楚，我还是先把临时变量声明为final，检查他们是否的确只被赋值一次：
 
```java
double getPrice() {
    final int basePrice = _quantity * _itemPrice;
    final double discountFactor;
    if (basePrice > 1000) discountFactor = 0.95;
    else discountFactor = 0.98;
    return basePrice * discountFactor;
} 
```


这样一来，如果有任何问题，编译器就会警告我。之所以先做这件事，因为如果临时变量不只被赋值一次，我就不该进行该项重构。接下来我开始替换临时变量，每次一个。首先我把赋值（assignment）动作的右侧表达式提炼出来：
 
```java
double getPrice() {
    final int basePrice = basePrice();
    final double discountFactor;
    if (basePrice > 1000) discountFactor = 0.95;
    else discountFactor = 0.98;
    return basePrice * discountFactor;
}

private int basePrice() {
    return _quantity * _itemPrice;
} 
```


编译并测试，然后开始使用[以查询取代临时变量](composing-methods.md#_8)。首先把临时变量basePrice的第一个引用点替换掉：
 
```java
double getPrice() {
    final int basePrice = basePrice();
    final double discountFactor;
    if (basePrice() > 1000) discountFactor = 0.95;
    else discountFactor = 0.98;
    return basePrice * discountFactor;
}
```
 

编译、测试、下一个（听起来像在指挥人们跳乡村舞蹈一样）。由于「下一个」已经是basePrice的最后一个引用点，所以我把basePrice临时变量的声明式一并摘除：
 
```java
double getPrice() {
    final double discountFactor;
    if (basePrice() > 1000) discountFactor = 0.95;
    else discountFactor = 0.98;
    return basePrice() * discountFactor;
    }
```
 

搞定basePrice之后，我再以类似办法提炼出一个discountFactor()：
 
```java
double getPrice() {
    final double discountFactor = discountFactor();
    return basePrice() * discountFactor;
}

private double discountFactor() {
    if (basePrice() > 1000) return 0.95;
    else return 0.98;
}
```
 

你看，如果我没有把临时变量basePrice替换为一个查询式，将多么难以提炼discountFactor()！
 

最终，getPrice()变成了这样：
 
```java
double getPrice() {
    return basePrice() * discountFactor();
}
```

## 以函数对象取代函数
--------------------


你有一个大型函数，其中对局部变量的使用，使你无法釆用 [提炼函数](composing-methods.md#_1)。
 
**将这个函数放进一个单独对象中，如此一来局部变量就成了对象内的值域（field） 然后你可以在同一个对象中将这个大型函数分解为数个小型函数。**
 
```java
class Order...
double price() {
    double primaryBasePrice;
    double secondaryBasePrice;
    double tertiaryBasePrice;
    // long computation;
    ...
}
```

![](../images/arrow.gif)
![](../images/06fig01.gif)

**动机（Motivation）**
 
我在本书中不断向读者强调小型函数的优美动人。只要将相对独立的代码从大型函数中提炼出来，就可以大大提高代码的可读性。
 
但是，局部变量的存在会增加函数分解难度。如果一个函数之中局部变量泛滥成灾, 那么想分解这个函数是非常困难的。[以查询取代临时变量](composing-methods.md#_8) 可以助你减轻这一负担，但有时候你会发现根本无法拆解一个需要拆解的函数。这种情况下，你应该把手深深地伸入你的工具箱（好酒沉瓮底呢），祭出函数对象（method object ）[Beck]这件法宝。
 
[以函数对象取代函数](composing-methods.md#_9) 会将所有局部变量都变成函数对象（method object）的值域（field）。然后你就可以对这个新对象使用 [提炼函数](composing-methods.md#_1) 创造出新函数，从而将原本的大型函数拆解变短。

 
**作法（Mechanics）**

我厚着脸皮从Kent Beck [Beck]那里偷来了下列作法：
 
- 建立一个新class，根据「待被处理之函数」的用途，为这个class命名。
 
- 在新class中建立一个final值域，用以保存原先大型函数所驻对象。我们将这个值域称为「源对象」。同时，针对原（旧）函数的每个临时变量和每个参数，在新中建立一个个对应的值域保存之。
 
- 在新class中建立一个构造函数（constructor），接收源对象及原函数的所有参数作为参数。
 
- 在新class中建立一个compute()函数。
 
- 将原（旧）函数的代码拷贝到compute()函数中。如果需要调用源对象的任何函数，请以「源对象」值域调用。
 
- 编译。
 
- 将旧函数的函数本体替换为这样一条语句：「创建上述新的一个新对象， 而后调用其中的compute()函数」。

 
现在进行到很有趣的部分了。由于所有局部变量现在都成了值域，所以你可以任意分解这个大型函数，不必传递任何参数。

 
**范例（Example）**
 
如果要给这一重构手法找个合适例子，需要很长的篇幅。所以我以一个不需要长篇幅（那也就是说可能不十分完美）的例子展示这项重构。请不要问这个函数的逻辑是什么，这完全是我且战且走的产品。
```java
Class Account
int gamma (int inputVal, int quantity, int yearToDate) {
    int importantValue1 = (inputVal * quantity) + delta();
    int importantValue2 = (inputVal * yearToDate) + 100;
    if ((yearToDate - importantValue1) > 100)
        importantValue2 -= 20;
    int importantValue3 = importantValue2 * 7;
    // and so on.
    return importantValue3 - 2 * importantValue1;
}
```
 
为了把这个函数变成一个函数对象（method object），我首先需要声明一个新class。在此新class中我应该提供一个final值域用以保存原先对象（源对象）；对于函数的每一个参数和每一个临时变量，也以一个个值域逐一保存。
 
```java 
class Gamma...
    private final Account _account;
    private int inputVal;
    private int quantity;
    private int yearToDate;
    private int importantValue1;
    private int importantValue2;
    private int importantValue3;
```
 
按惯例，我通常会以下划线作为值域名称的前缀。但为了保持小步前进，我暂时先保留这些值域的原名。

接下来，加入一个构造函数：
```java
Gamma (Account source, int inputValArg, int quantityArg, int yearToDateArg) {
    _account = source;
    inputVal = inputValArg;
    quantity = quantityArg;
    yearToDate = yearToDateArg;
}
```
 
现在可以把原本的函数搬到compute()了。函数中任何调用Account class的地方，我都必须改而使用_account值域：
```java 
int compute () {
    importantValue1 = (inputVal * quantity) + _account.delta();
    importantValue2 = (inputVal * yearToDate) + 100;
    if ((yearToDate - importantValue1) > 100)
        importantValue2 -= 20;
    int importantValue3 = importantValue2 * 7;
    // and so on.
    return importantValue3 - 2 * importantValue1;
}
```

然后，我修改旧函数，让它将它的工作转发〔委托，delegate）给刚完成的这个函 数对象（method object）：
```java
int gamma (int inputVal, int quantity, int yearToDate) {
    return new Gamma(this, inputVal, quantity, yearToDate).compute();
}
```

这就是本项重构的基本原则。它带来的好处是：现在我可以轻松地对compute()函数采取 [提炼函数](composing-methods.md#_1)，不必担心引数（argument）传递。

```java
int compute () {
    importantValue1 = (inputVal * quantity) + _account.delta();
    importantValue2 = (inputVal * yearToDate) + 100;
    importantThing();
    int importantValue3 = importantValue2 * 7;
    // and so on.
    return importantValue3 - 2 * importantValue1;
}

void importantThing() {
    if ((yearToDate - importantValue1) > 100)
        importantValue2 -= 20;
}
```

## 替换你的算法
--------------


把某个算法替换为另一个更清晰的算法。

**将函数本体（method body）替换为另一个算法。**

```java
String foundPerson(String[] people){
    for (int i = 0; i < people.length; i++) {
        if (people[i].equals ("Don")){
           return "Don";
        }
        if (people[i].equals ("John")){
           return "John";
        }
        if (people[i].equals ("Kent")){
           return "Kent";
        }
    }
    return "";
}
```

![](../images/arrow.gif)

```java
String foundPerson(String[] people){
    List candidates = Arrays.asList(new String[] {"Don", "John", "Kent"});
    for (int i=0; i<people.length; i++)
    if (candidates.contains(people[i]))
        return people[i];
    return "";
}
```


**动机（Motivation）**

我没试过给猫剥皮，不过我听说这有好几种方法，我敢打赌其中某些方法会比另一 些简单。算法也是如此。如果你发现做一件事可以有更清晰的方式，就应该以较清晰的方式取代复杂方式。「重构」可以把一些复杂东西分解为较简单的小块，但有 时你就是必须壮士断腕，删掉整个算法，代之以较简单的算法。随着对问题有了更 多理解，你往往会发现，在你的原先作法之外，有更简单的解决方案，此时你就需 要改变原先的算法。如果你开始使用程序库，而其中提供的某些功能/特性与你自 己的代码重复，那么你也需要改变原先的算法。

有时候你会想要修改原先的算法，让它去做一件与原先动作略有差异的事。这时候你也可以先把原先的算法替换为一个较易修改的算法，这样后续的修改会轻松许多。

使用这项重构手法之前，请先确定自己已经尽可能分解了原先函数。替换一个巨大而复杂的算法是非常困难的，只有先将它分解为较简单的小型函数，然后你才能很有把握地进行算法替换工作。


**作法（Mechanics）**

- 准备好你的另一个（替换用）算法，让它通过编译。
- 针对现有测试，执行上述的新算法。如果结果与原本结果相同，重构结束。
- 如果测试结果不同于原先，在测试和调试过程中，以旧算法为比较参照标准。
- 对于每个test case（测试用例），分别以新旧两种算法执行，并观察两者结果是否相同。这可以帮助你看到哪一个test case出现麻烦，以及出现了怎样的麻烦。

