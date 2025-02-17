The scoring logic for resumes in this script (`score_resume`) is based on evaluating various 
aspects of the resume, such as completeness of information, presence of keywords, work experience,
education, and additional criteria. Here's a breakdown of each aspect:

1. **Resume Completeness**:
   - If the resume contains sections like `Experience`, `Skills`, or `Education`, it is considered structured, similar to resumes on the `robota.ua` site. The script checks for six key sections: `Experience`, `Skills`, `Education`, `Languages`, `Additional Information`, and `Courses, trainings, certificates`. For each section found, **10 points** are awarded. If a section is missing, **2 points** are deducted.
   - If the resume does not contain these sections, it is considered less structured, similar to resumes on the `work.ua` site. In this case, the script checks for three basic sections: `Title`, `Name`, and `Details`. For each section found, **5 points** are awarded. If a section is missing, **2 points** are deducted.

2. **Keywords**:
   - The resume is analyzed for the presence of specific keywords, such as `Python`, `Django`, `REST API`, `SQL`, `JavaScript`, `Docker`, and `AWS`. For each keyword found, **5 points** are added. The search is case-insensitive to account for all possible variations in spelling.

3. **Work Experience**:
   - Work experience is measured based on the number of years mentioned in the resume:
     - If the experience is 5 years or more, **15 points** are added.
     - If the experience is between 3 and 5 years, **10 points** are added.
     - If the experience is less than 3 years, **5 points** are added.
   - The script considers mentions in both English (`years`) and Ukrainian (`років`).

4. **Education**:
   - If the resume mentions education, such as `Bachelor`, `Master`, `MCA`, `BCA`, `Computer Science`, or `Engineering`, **5 points** are added.

5. **Additional Criteria (Certificates, Courses)**:
   - If the resume mentions certificates or courses (`certificates` or `courses`), **3 points** are added for each mention.

The total points from all these criteria form the final score for the resume, which is then used 
to sort candidates by relevance.
