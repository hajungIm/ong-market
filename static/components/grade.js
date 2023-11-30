document.addEventListener('DOMContentLoaded', function () {
    var gradeElement =  document.querySelector('.profile_rank_eng');
    var grade = parseFloat(gradeElement.innerText);
    var letterGrade
    var color
    
      if (grade >= 4.5) {
        letterGrade = 'A+';
        color = 'green';
      } else if (grade >= 4.0) {
        letterGrade = 'A';
        color = 'green'; 
      } else if (grade >= 3.5) {
        letterGrade = 'B+';
        color = 'blue';
      } else if (grade >= 3.0) {
        letterGrade = 'B';
        color = 'blue';
      } else if (grade >= 2.5) {
        letterGrade = 'C+';
        color = '#E9BD15';
      } else if (grade >= 2.0) {
        letterGrade = 'C';
        color = '#E9BD15';
      } else if (grade >= 1.5) {
        letterGrade = 'D+';
        color = 'orange';
      } else if (grade >= 1.0) {
        letterGrade = 'D';
        color = 'orange';
      } else {
        letterGrade = 'F';
        color = 'red';
      }

    // 학점(A~F)으로 변환된 값을 출력하거나 필요한 작업을 수행하세요
    console.log('Numeric Grade:', grade);
    console.log('Letter Grade:', letterGrade);

    // 해당 DOM 요소에 학점을 적용하는 예시
    if (gradeElement) {
      gradeElement.textContent = letterGrade;
      gradeElement.style.color = color;
    }
  });