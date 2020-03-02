# Addendum

I've continued working through the Fast AI course, so I've learned many tips and best practices this repo doesn't embody. This document captures those nuances for my future self, and for any others who find this repo while researching for their own work.

## Working with time-series data

*This section isn't particularly relevant to this image classification project, but I felt it was generally a useful note*

Often a recurrent NN is used with time-series/sequential input data. 

[Part 1, lesson 6](https://github.com/hiromis/notes/blob/master/Lesson6.md#time-series-and-add_datepart-1321) mentions a useful trick: some features embedded in a date better describe time series data than the date itself. If the input data is properly annotated, we can entirely elide the need for a recurrent NN (or perhaps even outperform one).

The `add_datepart` Fast AI function adds lots of useful features describing a datetime, which an NN can then extract patterns from (day of week, day of month, is month start/end, month of year, is quarter start/end, etc).

## Classifying to a continuous variable (e.g.: solving a regression problem)

In [part 1, lesson 6](https://github.com/hiromis/notes/blob/master/Lesson6.md#categorical-and-continuous-variables-2223) ([video](https://course.fast.ai/videos/?lesson=6) transcript keyword "regression") it was noted that labels annotated as a `FloatList` will automatically be treated as a regression (rather than classification) problem.

This project's first build log used the `FloatList` configuration (because the data annotations were scalar, rather than categorical enums), but I pieced together my image regression pipeline using function documentation I didn't fully understand. Because my attempt at image regression failed, I suggest looking at Fast AI lesson 6's rich, working example of regression on tabular data (a somewhat different problem domain, but hopefully similar enough to be useful).

*Helpful suggestions:*

Consider setting [`log=true`](https://github.com/hiromis/notes/blob/master/Lesson6.md#reminder-about-doc-2509) when setting up `FloatList` labels (e.g.: `.label_from_df(cols=dep_var, label_cls=FloatList, log=True)`). This ensures the classifier won't be too thrown-off by long-tail examples, since performance will be measured in a way that accounts for orders of magnitude (e.g.: off by $5 on $1,000,000 is negligible, while off by $5 on $2 is huge). This is useful when predicting population, sales numbers, prices, or anything with a wide (unbounded, even) distribution of values.

If your data has a known range of values, consider setting [`y_range`](https://github.com/hiromis/notes/blob/master/Lesson6.md#y_range-2712) when constructing your learner. This ensures predictions map into that fixed range, hopefully improving model performance. If you set `log=true` on the dataset labels, your `y_range` needs to be log scaled, too (e.g.: use `np.log` on the min and max values in the range).
