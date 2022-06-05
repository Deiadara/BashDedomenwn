CREATE OR REPLACE VIEW projects_per_organization_per_year (organization_id, organization_name, projects, yearr)
AS
SELECT o.organization_id, o.orgname, COUNT(*), y.year_id as yearr 
FROM organization o INNER JOIN project p ON o.organization_id = p.org_id
INNER JOIN years y ON DATEDIFF(y.year_id,p.start_date)>0 and DATEDIFF(y.year_id,p.finish_date)<0
GROUP BY o.organization_id, yearr;


CREATE OR REPLACE VIEW sci_fields_couples (first_field, second_field, projects)
AS
SELECT s.scientific_field_id as first_field, ss.scientific_field_id as second_field, COUNT(*) as projects
FROM scientific_field s INNER JOIN scientific_field ss 
INNER JOIN field_of_project  f ON (s.scientific_field_id = f.scientific_field_id or ss.scientific_field_id = f.scientific_field_id  )
WHERE s.scientific_field_id != ss.scientific_field_id
GROUP BY s.scientific_field_id, ss.scientific_field_id
ORDER BY projects DESC;


CREATE OR REPLACE VIEW no_deliverables (project_id, project_title, finish_date, start_date )
AS
SELECT a.project_id, a.project_title, a.finish_date, a.start_date
FROM project a 
WHERE a.project_id NOT IN 
(SELECT c.project_id FROM deliverable c WHERE c.date>CURDATE());

CREATE OR REPLACE VIEW organizations (organization_id, orgname, project_id, project_title )
AS 
SELECT organization.organization_id , organization.orgname,project.project_id, project.project_title
 FROM organization INNER JOIN project ON project.org_id = organization.organization_id 
 ORDER BY organization.orgname;

CREATE OR REPLACE VIEW researchers (researcher_id, researcher_name, surname, project_id, project_title )
AS 
SELECT researcher.researcher_id, researcher.researcher_name , researcher.surname,project.project_id, project.project_title
 FROM researcher INNER JOIN works_in_project ON works_in_project.researcher_id = researcher.researcher_id 
 INNER JOIN project ON project.project_id = works_in_project.project_id
 ORDER BY researcher_id