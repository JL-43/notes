# Latest Article

# Understanding Isolation in ACID Transactions

When databases perform multiple tasks at the same time, isolation ensures that each task doesn't mess up the others. Imagine working on a group project where everyone needs to focus on their part without interruptions. This document breaks down these concepts to make them easier to understand.

---

## **Easy Analogy: Library Study Rooms**

Picture this: you're in a library, using a quiet study room:

1. **Dirty Reads**:
   - You're reading a draft of a book that someone else slid under your door. Later, they tell you the draft was full of mistakes.

2. **Non-Repeatable Reads**:
   - You check the catalog and see a book is available. When you go to grab it, someone else has already borrowed it.

3. **Phantom Reads**:
   - You search for all books on a topic and find 10. While deciding, someone adds another book, so now there are 11.

4. **Lost Updates**:
   - You and a friend edit the same book. You write a note on page 10, but their notes overwrite yours.

---

## **What Can Go Wrong?**

1. **Dirty Reads**:
   - Reading unfinished changes.
   - Problem: Acting on bad data.

2. **Non-Repeatable Reads**:
   - Data changes between your checks.
   - Problem: Inconsistent info.

3. **Phantom Reads**:
   - New data shows up during your task.
   - Problem: Your results might miss something.

4. **Lost Updates**:
   - Two tasks change the same data, but only one gets saved.
   - Problem: Important updates disappear.

---

## **Levels of Isolation**

Databases handle isolation with different levels. Here's a quick look:

| Isolation Level    | Dirty Reads | Non-Repeatable Reads | Phantom Reads | Lost Updates |
| ------------------ | ----------- | -------------------- | ------------- | ------------ |
| Read Uncommitted   | ✔️          | ✔️                   | ✔️            | ✔️           |
| Read Committed     | ❌          | ✔️                   | ✔️            | ✔️           |
| Repeatable Read    | ❌          | ❌                   | ✔️            | ❌           |
| Snapshot Isolation | ❌          | ❌                   | ❌ (mostly)   | ❌           |
| Serializable       | ❌          | ❌                   | ❌            | ❌           |

✔️ = Can Happen, ❌ = Prevented

---

### **Details of Each Level**

1. **Read Uncommitted**:
   - Reads changes even if they're not finished.
   - Problems: Dirty reads, inconsistent data.
   - Good for: Quick, low-risk tasks.

2. **Read Committed**:
   - Reads only finished changes.
   - Problems: Data might change mid-task.
   - Good for: Balancing speed and accuracy.

3. **Repeatable Read**:
   - Sees the same data throughout the task.
   - Problems: New data can still appear.
   - Good for: Finances or important records.

4. **Snapshot Isolation**:
   - Each task gets its own snapshot of data.
   - Problems: Rare phantom data issues.
   - Good for: Big reports or analysis.

5. **Serializable**:
   - Treats each task as if it's running alone.
   - Problems: Slower performance.
   - Good for: Critical operations where mistakes can't happen.

---

## **How It's Done**

1. **Locks**:
   - Stops others from using the data you're changing.
   - Example:
     ```
     BEGIN TRANSACTION;
     LOCK TABLE accounts;
     UPDATE accounts SET balance = balance - 100 WHERE id = 1;
     COMMIT;
     ```

2. **Multiversion Concurrency Control (MVCC)**:
   - Everyone sees their own version of the data.
   - Example:
     ```
     BEGIN TRANSACTION;
     SELECT * FROM orders AS OF SYSTEM_TIME '2024-01-01T00:00:00';
     UPDATE orders SET status = 'processed' WHERE id = 101;
     COMMIT;
     ```

3. **Timestamp Ordering**:
   - Decides who gets to change data based on time.
   - Example:
     ```
     BEGIN TRANSACTION;
     SELECT current_timestamp;
     IF transaction_timestamp < last_committed_timestamp THEN
       ROLLBACK;
     ELSE
       INSERT INTO logs (event) VALUES ('transaction approved');
       COMMIT;
     END IF;
     ```

---

## **Choosing the Right Level**

- **Read Uncommitted/Read Committed**:
   - Fast but might lead to errors.

- **Repeatable Read**:
   - Slower but safer for important tasks.

- **Serializable**:
   - Very safe but can slow everything down.

Pick the level that works best for what you're doing!

---

## **Want to Learn More?**

- **Books**:
  - "Database System Concepts" by Silberschatz, Korth, and Sudarshan
  - "Transaction Processing: Concepts and Techniques" by Jim Gray and Andreas Reuter

- **Online Resources**:
  - [ACID Transactions - Wikipedia](https://en.wikipedia.org/wiki/ACID)
  - [Isolation Levels in SQL Server - Microsoft Docs](https://learn.microsoft.com/en-us/sql/t-sql/statements/set-transaction-isolation-level-transact-sql)

- **Research Papers**:
  - "A Critique of ANSI SQL Isolation Levels" by Hal Berenson et al.
  - "Consistency in Database Systems" by Theo Haerder and Andreas Reuter



# Table of Contents

