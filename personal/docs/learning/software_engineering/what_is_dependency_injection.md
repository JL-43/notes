---
tags:
  - Software Engineering
  - Informational
---

# Dependency Injection Demystified

*A Note from JL: I did not write this article, but the page it is from is fairly old and is on `http`. So I wanted to move it somewhere more accessible :)*

*March 21, 2006*

When I first heard about dependency injection, I thought, "Dependendiwhatsit?" and promptly forgot about it. When I finally took the time to figure out what people were talking about, I laughed. "That's all it is?"

"Dependency Injection" is a 25-dollar term for a 5-cent concept. That's not to say that it's a bad term... and it's a good tool. But the top articles on Google focus on bells and whistles at the expense of the basic concept. I figured I should say something, well, simpler.

## The Really Short Version

Dependency injection means giving an object its instance variables. Really. That's it.

## The Slightly Longer Version, Part I: Dependency Non-Injection

Classes have these things they call methods on. Lets call those "dependencies." Most people call them "variables." Sometimes, when they're feeling fancy, they call them "instance variables."

```java
public class Example {
  private DatabaseThingie myDatabase;

  public Example() {
    myDatabase = new DatabaseThingie();
  }

  public void DoStuff() {
    ...
    myDatabase.GetData();
    ...
  }
}
```

Here, we have a variable... uh, dependency... named "myDatabase." We initialize it in the constructor.

## The Slightly Longer Version, Part II: Dependency Injection

If we wanted to, we could pass the variable into the constructor. That would "inject" the "dependency" into the class. Now when we use the variable (dependency), we use the object that we were given rather than the one we created.

```java
public class Example {
  private DatabaseThingie myDatabase;

  public Example() {
    myDatabase = new DatabaseThingie();
  }

  public Example(DatabaseThingie useThisDatabaseInstead) {
    myDatabase = useThisDatabaseInstead;
  }

  public void DoStuff() {
    ...
    myDatabase.GetData();
    ...
  }
}
```

That's really all there is to it. The rest is just variations on the theme. You could set the dependency (<cough> variable) in... wait for it... a setter method. You could set the dependency by calling a setter method that's defined in a special interface. You can have the dependency be an interface and then polymorphically pass in some polyjuice. Whatever.

## The Slightly Longer Version, Part III: Why Do We Do This?

Among other things, it's handy for isolating classes during testing.

```java
public class ExampleTest {
  TestDoStuff() {
    MockDatabase mockDatabase = new MockDatabase();

    // MockDatabase is a subclass of DatabaseThingie, so we can
    // "inject" it here:
    Example example = new Example(mockDatabase);

    example.DoStuff();
    mockDatabase.AssertGetDataWasCalled();
  }
}

public class Example {
  private DatabaseThingie myDatabase;

  public Example() {
    myDatabase = new DatabaseThingie();
  }

  public Example(DatabaseThingie useThisDatabaseInstead) {
    myDatabase = useThisDatabaseInstead;
  }

  public void DoStuff() {
    ...
    myDatabase.GetData();
    ...
  }
}
```

That's it. Dependency injection is really just passing in an instance variable.

## Further Reading

There's a lot of ways to make this simple concept very complicated. (There's lots of ways to make any concept complicated! Simplicity is hard.) Sometimes such complexity is necessary... and it's never my first choice. I've chosen not to discuss those bells and whistles here, but if you really want to know, check out:

*Inversion of Control Containers and the Dependency Injection Pattern*. Martin Fowler is my favorite author. Usually he's clear and concise. Here he succeeds in making dependency injection sound terribly complicated. Still, this article has a thorough discussion of the various ways dependency injection can be tweaked.

*Updated 3 Nov, 2024: Remove broken link to further reading.*

*Updated 25 Mar, 2006: Added references to further reading.*

---

*Original article by James Shore*
