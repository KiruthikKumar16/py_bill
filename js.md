# JavaScript & Frontend — Interview Notes

*Companion notes to the Full Stack Prep Checklists. Read a section, then explain it out loud to yourself before moving on — if you can't explain it simply, you don't know it yet.*

---

## 1. HTML/CSS Quick Refresher

- **Box model:** every element = content → padding → border → margin. `box-sizing: border-box` makes width/height include padding+border (almost always what you want).
- **Flexbox basics:** `display: flex` on a parent; `justify-content` controls the main axis, `align-items` controls the cross axis. `flex: 1` makes a child grow to fill space.
- **Position:** `static` (default) → `relative` (offsets from normal position, still takes up space) → `absolute` (removed from flow, positioned relative to nearest positioned ancestor) → `fixed` (relative to viewport).

**Likely interview question:** "How do you center a div?" → `display: flex; justify-content: center; align-items: center;` on the parent.

---

## 2. JavaScript Fundamentals

### Variables
```js
var x = 1;   // function-scoped, hoisted, avoid using
let y = 2;   // block-scoped, can reassign
const z = 3; // block-scoped, cannot reassign (but object/array contents CAN change)
```
`const arr = [1,2]; arr.push(3);` is legal — you're mutating contents, not reassigning `arr`.

### Hoisting
Function declarations and `var` are hoisted (moved to the top of their scope during compile). `let`/`const` are hoisted too but sit in a "temporal dead zone" — accessing them before declaration throws an error, unlike `var` which gives `undefined`.

### `==` vs `===`
`===` checks value AND type, no conversion. `==` does type coercion first (`'5' == 5` → true). **Always use `===`** unless you have a specific reason not to. This is a very common interview question.

### Functions & `this`
```js
function regular() { console.log(this); }      // `this` depends on how it's called
const arrow = () => { console.log(this); };     // `this` is inherited from enclosing scope, never rebound
```
Arrow functions don't have their own `this` — this is exactly why they're preferred inside callbacks (e.g., inside a `setTimeout` or array method) when you want `this` to still refer to the outer context.

### Closures
A closure is a function that "remembers" variables from the scope it was created in, even after that scope has finished executing.
```js
function counter() {
  let count = 0;
  return function() {
    count++;
    return count;
  };
}
const increment = counter();
increment(); // 1
increment(); // 2 — count persisted between calls
```
**This is one of the single most common JS interview questions.** Be ready to explain it and write one from scratch.

---

## 3. Arrays & Objects

### Common array methods (know these cold)
```js
arr.map(x => x * 2);              // transform each item, returns new array
arr.filter(x => x > 5);           // keep items matching condition
arr.reduce((acc, x) => acc + x, 0); // combine into a single value
arr.find(x => x.id === 3);        // first match or undefined
arr.some(x => x > 10);            // true if ANY match
arr.every(x => x > 0);            // true if ALL match
```

### Destructuring & spread/rest
```js
const { name, age } = person;        // object destructuring
const [first, second] = arr;         // array destructuring
const merged = { ...obj1, ...obj2 }; // spread — shallow merge
function sum(...nums) { ... }        // rest — collects args into array
```

### Shallow vs deep copy
`{ ...obj }` and `[...arr]` are **shallow** copies — nested objects/arrays still share references. This trips people up in interviews when they mutate a "copy" and the original changes too.

---

## 4. Asynchronous JavaScript

This is a heavily-tested area. Know the progression:

**Callbacks → Promises → async/await** (same underlying mechanism, increasingly readable syntax)

```js
// Promise
fetch('/api/users')
  .then(res => res.json())
  .then(data => console.log(data))
  .catch(err => console.error(err));

// async/await (same thing, cleaner)
async function getUsers() {
  try {
    const res = await fetch('/api/users');
    const data = await res.json();
    console.log(data);
  } catch (err) {
    console.error(err);
  }
}
```

### Event loop (conceptual — very common interview topic)
JS is single-threaded. The **call stack** runs synchronous code. Async operations (timers, fetch, promises) get handed off, and their callbacks go into a **queue**. The event loop only pushes queued callbacks onto the stack once the stack is empty.

Classic gotcha question:
```js
console.log('1');
setTimeout(() => console.log('2'), 0);
console.log('3');
// Output: 1, 3, 2 — even with 0ms delay, setTimeout callback waits for the stack to clear
```

---

## 5. DOM & Events

```js
document.querySelector('.btn');        // first match
document.querySelectorAll('.item');    // all matches (NodeList)
element.addEventListener('click', handler);
```

- **Event bubbling:** events propagate from the target element up through its ancestors. `event.stopPropagation()` stops this.
- **Event delegation:** attach one listener to a parent instead of many to children, and check `event.target` inside the handler. More efficient, and works for dynamically-added elements.

---

## 6. ES6+ Features Worth Knowing

- Template literals: `` `Hello ${name}` ``
- Default parameters: `function greet(name = 'friend') {}`
- Classes (syntactic sugar over prototypes):
```js
class Animal {
  constructor(name) { this.name = name; }
  speak() { return `${this.name} makes a sound`; }
}
class Dog extends Animal {
  speak() { return `${this.name} barks`; }
}
```
- Modules: `import`/`export`

---

## 7. React Basics (if it's on the resume)

### Components & Props
```jsx
function Greeting({ name }) {
  return <h1>Hello, {name}</h1>;
}
```
Props flow **down** only — a child can't directly change a parent's props.

### State
```jsx
import { useState } from 'react';

function Counter() {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount(count + 1)}>{count}</button>;
}
```
- State updates are **asynchronous and batched** — don't expect `count` to reflect the new value immediately after calling `setCount`.
- Never mutate state directly (`state.push(x)` ❌). Always create a new array/object.

### useEffect
```jsx
useEffect(() => {
  fetchData();
}, [someValue]); // runs on mount + whenever someValue changes
```
Empty array `[]` = runs once on mount. No array = runs on every render. Be ready to explain the dependency array — it's a common interview probe.

### Lifting state up
When two sibling components need to share data, move the state to their common parent and pass it down via props, along with a callback function to update it.

### Lists & keys
```jsx
items.map(item => <li key={item.id}>{item.name}</li>)
```
`key` must be stable and unique — don't use array index if the list can reorder.

---

## 8. Common "Gotcha" Interview Questions

| Question | Short answer |
|---|---|
| `null` vs `undefined`? | `undefined` = declared but not assigned. `null` = intentionally set to "no value." |
| What is NaN? | "Not a Number" — result of an invalid math operation. `typeof NaN === 'number'` (yes, really). |
| Explain event loop | See Section 4 |
| What is a closure? | See Section 2 |
| var vs let vs const? | Scope + reassignment rules — see Section 2 |
| What is hoisting? | See Section 2 |
| Difference between `map` and `forEach`? | `map` returns a new array; `forEach` returns `undefined` and is used purely for side effects |
| What's a pure function? | Same input always gives same output, no side effects |

---

## How to Study This
1. Read a section.
2. Close the notes, explain it out loud in your own words.
3. Write the code example from memory.
4. If you get stuck, that's the gap — go back and re-read only that part.
