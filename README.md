Logs Analysis Project

This code search informations in a database, there are here the 3 questions asked.

What are the most popular three articles of all time?
Who are the most popular article authors of all time?
On which days did more than 1% of requests lead to errors?

Open output_example.txt to see a dump of the expected output after running log_analysis.py.

• Download and install VM using [VirtualBox](https://www.virtualbox.org/wiki/Downloads)  
• Download and install [Vagrant](https://www.vagrantup.com/downloads.html) for the VM settings   
• Run in the working folder `vagrant up` to configure the VM  
• Run `vagrant ssh` to log into the VM  
• Download the [news data](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)  and save it 
• in the working VM folder.
• Run psql -d news -f newsdata.sql to generate the database
• Then Run the logsanalysis.py python code.





This the differents views created in my projects:


View 1 :

CREATE VIEW pop_articles AS
SELECT articles.title,
       COUNT(log.path) AS views
FROM articles
LEFT JOIN log ON '/article/' || articles.slug = log.path
GROUP BY articles.title
ORDER BY views DESC
LIMIT 3;

View 2 :

CREATE VIEW pop_authors AS
SELECT authors.name,
       article_author.views
FROM authors,
  (SELECT articles.author,
          COUNT(log.path) AS views
   FROM articles
   LEFT JOIN log ON '/article/' || articles.slug = log.path
   GROUP BY articles.author
   ORDER BY views DESC) AS article_author
WHERE article_author.author = authors.id;

View 3 :

CREATE VIEW one_percent_errors AS WITH
NORMAL AS
  (SELECT date(TIME) AS log_date,
          COUNT(*) AS day_logs
   FROM log
   GROUP BY log_date), errors AS
  (SELECT DATE(TIME) AS log_date,
          COUNT(TIME) AS day_error_logs
   FROM log
   WHERE to_number(substr(status, 1, 3), '999') >= 400
   GROUP BY log_date),
                       calc AS
  (SELECT ((errors.day_error_logs * 100.) / normal.day_logs) AS percent,
          normal.log_date AS log_date
   FROM
   NORMAL
   JOIN errors USING (log_date))
SELECT calc.log_date,
       ROUND(calc.percent::NUMERIC,1)
FROM calc
WHERE (calc.percent > 1);
