// let a = 'show';

// function toggleSidebar() {
//     const sidebar = document.querySelector('.sidebar');
//     a = a === 'show' ? 'none' : 'show';
//     sidebar.style.display = a;
// }

// function setDisplayNone() {
//     a = 'none';
//     document.querySelector('.sidebar').style.display = a;
// }

// function setDisplayShow() {
//     a = 'show';
//     document.querySelector('.sidebar').style.display = a;
// }

// function handleHomeClick() {
//     if (a === 'show') {
//         setDisplayNone();
//         setTimeout(() => {
//             document.querySelector('.sidebar').remove();
//         }, 300);
//     }
//     // 추가로 Home 버튼을 클릭했을 때 수행할 작업이 있다면 여기에 추가
// }

// function handleMusicClick() {
//     if (a === 'none') {
//         setDisplayShow();
//     }
//     // 추가로 Music 버튼을 클릭했을 때 수행할 작업이 있다면 여기에 추가
// }



// function show(){
//     document.getElementById(".sidebar").style.display ='block';
// }
// function hide(){
//     document.getElementById(".sidebar").style.display ='none';
// }


// function showHide(){
//     if(document.getElementById("showHide").style.display =='none'){
//         document.getElementById("showHide").style.display ='block';
//     }
//     else{
//         document.getElementById("showHide").style.display ='none';
//     }
// }



// function toggleSidebar(displayValue) {
//     document.querySelector('.sidebar').style.display = displayValue;
// }



// const showMenu = (toggleId, navbarId, bodyId) => {
//     const toggle = document.getElementById(toggleId),
//         navbar = document.getElementById(navbarId),
//         bodypadding = document.getElementById(bodyId);

//     // 페이지 로딩 시 Expander 상태 설정
//     const isExpanderOpen = sessionStorage.getItem('isExpanderOpen') === 'true';
//     if (isExpanderOpen) {
//         navbar.classList.add('expander');
//     }

//     if (toggle && navbar) {
//         toggle.addEventListener('click', (event) => {
//             event.preventDefault();  // 기본 동작 중지

//             navbar.classList.toggle('expander');
//             bodypadding.classList.toggle('body-pd');

//             // Expander 상태 저장
//             const isExpanderOpen = navbar.classList.contains('expander');
//             sessionStorage.setItem('isExpanderOpen', isExpanderOpen.toString());

//             // console.log('showMenu 함수가 호출되었습니다.');
//         });
//     }
// };

// // showMenu 함수 호출
// showMenu('nav-toggle', 'navbar', 'body-pd');


/* EXPANDER MENU */
const showMenu = (toggleId, navbarId, bodyId) => {
    const toggle = document.getElementById(toggleId),
    navbar = document.getElementById(navbarId),
    bodypadding = document.getElementById(bodyId)

    if( toggle && navbar ) {
        toggle.addEventListener('click', ()=>{
            navbar.classList.toggle('expander');

            bodypadding.classList.toggle('body-pd')
        })
    }
}

showMenu('nav-toggle', 'navbar', 'body-pd')


/* LINK ACTIVE */
const linkColor = document.querySelectorAll('.nav__link')
function colorLink() {
    linkColor.forEach(l=> l.classList.remove('active'))
    this.classList.add('active')
}
linkColor.forEach(l=> l.addEventListener('click', colorLink))





/* COLLAPSE MENU */
// const linkCollapse = document.getElementsByClassName('collapse__link')
// var i

// for(i=0;i<linkCollapse.length;i++) {
//     linkCollapse[i].addEventListener('click', function(){
//         const collapseMenu = this.nextElementSibling
//         collapseMenu.classList.toggle('showCollapse')

//         const rotate = collapseMenu.previousElementSibling
//         rotate.classList.toggle('rotate')
//     });
// }


// function authenticateSpotify() {
//     fetch('/spotify/is-authenticated')
//     .then((response) => response.json())
//     .then((data) => {
//         this.setState({ spotifyAuthenticated: data.status});
//         if (!data.status) {
//             fetch('/spotify/get-auth-url')
//             .then((response) => response.json())
//             .then((data)=>{
//                 window.location.replace(data.url);
//             });
//         }
//     });
// }


// main.js

// function authenticateSpotify() {
//     fetch('/spotify/is-authenticated')
//         .then((response) => response.json())
//         .then((data) => {
//             // Handle the authentication data as needed
//             if (!data.status) {
//                 fetch('/spotify/get-auth-url')
//                     .then((response) => response.json())
//                     .then((data) => {
//                         window.location.replace(data.url);
//                     });
//             }
//         });
// }

// 로그인 기능 구현

// function authenticateSpotify() {
//     fetch(`/spotify/is-authenticated`)
//       .then((response) => response.json())
//       .then((data) => {
//         console.log(data.status);
//         if (!data.status) {
//           fetch(`/spotify/get-auth-url`)
//             .then((response) => response.json())
//             .then((data) => {
//               window.location.replace(data.url);
//             });
//         }
//       });
//   }


// var ctx = document.getElementById('genre_cnt_chart').getContext('2d');
// var genrepieChart = new Chart(ctx, {
//     type: 'doughnut',
//     data: {
//         labels: genre_label,
//         datasets: [{
//             label: 'genre',
//             data: genre_cnt,
//             backgroundColor: [
//                 'rgb(255, 99, 132)', 'rgb(255, 159, 64)', 'rgb(255, 205, 86)', 'rgb(75, 192, 192)',
//                 'rgb(54, 162, 235)', 'rgb(153, 102, 255)', "#8e5ea2", "#3cba9f", "#e8c3b9", "#c45850"
//             ],
//             hoverOffset: 4
//         }]
//     },
//     options: {
//         responsive: false,
//     }
// });


// history.back();

function draw_comparing_graphs()
{
    window.open('','_self', 'location=yes,height=300,width=500,scrollbars=yes,status=yes');  
}


function moveClose() {
    opener.location.href="/main";
    self.close();
}


function showAlert2() {
    alert("플레이리스트에서 제거되었습니다.");
}

function hrefLink() {
	location.href = '/music';
}



var $star_rating = $('.star-rating .fa');

var SetRatingStar = function() {
  return $star_rating.each(function() {
    if (parseInt($star_rating.siblings('input.rating-value').val()) >= parseInt($(this).data('rating'))) {
      return $(this).removeClass('fa-star-o').addClass('fa-star');
    } else {
      return $(this).removeClass('fa-star').addClass('fa-star-o');
    }
  });
};

$star_rating.on('click', function() {
  $star_rating.siblings('input.rating-value').val($(this).data('rating'));
  return SetRatingStar();
});

SetRatingStar();


function validateForm() {
  // 선택된 값이 있는지 확인
  var selectedRating = document.querySelector('input[name="rating_score"]:checked');
  
  if (!selectedRating) {
      // 선택된 값이 없으면 경고 표시 및 제출 막기
      alert('별점을 선택하세요.');
      return false;
  } else {
  // 선택된 값이 있으면 제출 허용
  alert('플레이리스트에 추가되었습니다.')
  return true;
  }
}

