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

***

Логика начисления очков за резюме в этом скрипте (`score_resume`) строится на оценке различных 
аспектов резюме, таких как полнота информации, наличие ключевых слов, опыт работы, образование 
и дополнительные критерии. Рассмотрим каждый из этих аспектов:

1. **Полнота резюме**:
   - Если резюме содержит разделы `Experience`, `Skills`, или `Education`, то оно считается структурированным, как на сайте `robota.ua`. Для таких резюме скрипт проверяет наличие шести ключевых разделов: `Experience`, `Skills`, `Education`, `Languages`, `Additional Information`, и `Courses, trainings, certificates`. За каждый найденный раздел начисляется **10 очков**. Если раздел отсутствует, отнимается **2 очка**.
   - Если резюме не содержит указанных разделов, оно считается менее структурированным, как на сайте `work.ua`. В этом случае проверяются три базовых раздела: `Title`, `Name`, и `Details`. За каждый найденный раздел начисляется **5 очков**. Если раздел отсутствует, отнимается **2 очка**.

2. **Ключевые слова**:
   - Резюме анализируется на наличие ключевых слов, таких как `Python`, `Django`, `REST API`, `SQL`, `JavaScript`, `Docker`, и `AWS`. За каждое найденное ключевое слово добавляется **5 очков**. Поиск осуществляется с учетом регистра, чтобы учесть все возможные варианты написания.

3. **Опыт работы**:
   - Опыт работы измеряется на основе количества лет, упомянутых в резюме:
     - Если опыта 5 и более лет, добавляется **15 очков**.
     - Если опыта от 3 до 5 лет, добавляется **10 очков**.
     - Если опыта менее 3 лет, добавляется **5 очков**.
   - Скрипт учитывает упоминания как на английском (`years`), так и на украинском (`років`).

4. **Образование**:
   - Если в резюме упоминается образование, например, `Bachelor`, `Master`, `MCA`, `BCA`, `Computer Science`, или `Engineering`, добавляется **5 очков**.

5. **Дополнительные критерии (сертификаты, курсы)**:
   - Если в резюме упоминаются сертификаты или курсы (`certificates` или `courses`), за каждое такое упоминание добавляется **3 очка**. 

Сумма очков за все критерии формирует финальную оценку резюме, которая затем используется 
для сортировки кандидатов по релевантности.