# Addendum

This document contains new things I've learned as I've worked further in the Fast AI course. I plan to add useful information that stands out to me, and information that clarifies things I didn't fully understand when originally working on this project.

## Working with time-series data

Often a recurrent NN is used with time-series/sequential input data. 

[Part 1, lesson 6](https://github.com/hiromis/notes/blob/master/Lesson6.md#time-series-and-add_datepart-1321) mentions a useful trick: often some feature embedded in a date better describes time series data than the date itself. If the input data is properly annotated, we can elide the need for a recurrent NN. The `add_datepart` Fast AI function adds lots of useful features describing a datetime for the NN to extract patterns from (day of week, day of month, is month start/end, month of year, is quarter start/end, etc).

## Classifying to a continuous variable (e.g.: solving a regression problem)

In [part 1, lesson 6](https://github.com/hiromis/notes/blob/master/Lesson6.md#categorical-and-continuous-variables-2223) (video transcript keyword "regression") it was noted that labels annotated as a float list will automatically be treated as a regression (rather than classification) problem. This was done in build log 1 (with a comment that the classes were scalar values, rather than enums), but I didn't fully understand what I was doing. Lesson 6 gives a rich, working example of a regression problem using tabular input data.

*Helpful suggestion:* set `log=true` when setting up labels (e.g.: `.label_from_df(cols=dep_var, label_cls=FloatList, log=True)`). This ensures the classifier won't be too thrown-off by long-tail examples, and instead focuses on orders of magnitude and percentage differences. This is useful for making fuzzy predictions where the input data simply can't be the whole picture (so precise input->output value mappings are a fool's errand), but we still want a somewhat fuzzy output to act on.
