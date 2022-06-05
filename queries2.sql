SELECT a.researcher_name, a.surname, COUNT(b.project_id) FROM researcher a 
INNER JOIN works_in_project b ON a.researcher_id = b.researcher_id 
INNER JOIN project c ON c.project_id = b.project_id 
WHERE c.finish_date > CURDATE() AND DATEDIFF(CURDATE(),a.date_of_birth) /365 < 40 
GROUP BY a.researcher_id 
ORDER BY COUNT(b.project_id) DESC;

SELECT r.researcher_id, r.researcher_name,r.surname, COUNT(b.project_id) 
FROM researcher r INNER JOIN works_in_project w ON r.researcher_id = w.researcher_id 
INNER JOIN no_deliverables b ON w.project_id = b.project_id
GROUP BY r.researcher_id
ORDER BY COUNT(b.project_id) DESC ;

SELECT c.orgname, b.member_id, SUM(a.amount)
FROM project a INNER JOIN management b  ON b.project_id = a.project_id  
INNER JOIN organization c ON a.org_id = c.organization_id WHERE c.orgtype = "Εταιρεία" 
group by a.org_id, b.member_id 
ORDER BY SUM(a.amount) DESC;

select o.organization_name, o.organization_id, o.projects, o.yearr FROM 
projects_per_organization_per_year o INNER JOIN projects_per_organization_per_year y
ON o.organization_id = y.organization_id
WHERE o.projects=y.projects AND o.projects>=10 AND YEAR(o.yearr)-YEAR(y.yearr)=-1;


SELECT * FROM sci_fields_couples;

SELECT p.project_title, r.researcher_name, r.surname FROM 
            field_of_project fp INNER JOIN project p ON p.project_id = fp.project_id
            INNER JOIN works_in_project wp ON p.project_id = wp.project_id
            INNER JOIN researcher r ON wp.researcher_id = r.researcher_id
            WHERE p.start_date < CURDATE() and p.finish_date> CURDATE() and fp.scientific_field_id = 1
            ORDER BY p.project_title