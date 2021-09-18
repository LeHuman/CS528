## CS528 - Data Privacy and Security

Illinois Institute of Technology

Homework 1

9-17-21

### What this is

An exercise on data anonymization using k-anonymity, entropy l-diversity, and recursive c-l diversity

### Requirements

Python 3.9.x

Note: These scripts were made on Windows, but should all work fine elsewhere

### How to run

Ensure the data is in the same directory under the folder `data`

Run main.py with a parameter 1-5 to run the respective task

> python main.py [1-5]

If this is a submission, just run the appropriate main.py

> python hw1-1-main.py

### How it works

The given data set is formatted as such

> age, workclass, fnlwgt, education, education-num, marital-status, occupation, relationship, race, sex, capital-gain, capital-loss, hours-per-week, native-country, salary

The data is then cut down to only include the following values

> age, education, marital_status, occupation, race, k-min

Where `occupation` is the SA and the rest are QIs with the exception of k-min; this is determined per user based off their salary

Each line is converted to a `User` object which is used to treat each line as an individual user within this dataset.
The `User` keeps track of it's `Attributes` (aka QIs) which in turn also keep track of the generalization that it is currently at.

The main loop in this implementation goes through each `User` matching them up with `User`s that have the same QIs.

`User`s in this data set are matched together if they have the same attributes ( same including whether their current generalized values are the same ).
`User`s that are matched up *merge* together to form a q*-block. The head `User` keeps track of the number of `User`s that have merged with it by using a count of the number of `User`s, a py `Counter` obj for keeping track of the SAs, and a list of all the `User`s under it, including itself.

A `User` / q*-block is considered satisfied if it meets all of it's criteria with k-anonymity, l-diversity, or recursive c-l diversity after attempting to match with all users.

If a `User` / q*-block is not satisfied, it can increase the generatively of the attribute that would cause the least distortion and then attempt to match again.

This process loops until every `User` / q*-block is satisfied or if users are no longer matching.

### Note about submissions

The instructions asked for two separate source files for each submission.

The way I set this up only requires a change in argument for both submissions, meaning they are the same source files.

I am also unable to set the prefix `hw1-1-` to each source file, as Python does not let me import if I do so