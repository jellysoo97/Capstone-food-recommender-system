import React, { useState, useEffect } from "react"
import { useNavigate } from "react-router-dom"
import axios from "axios"
import { Rating } from 'react-simple-star-rating'
import "../../index.css"

function Result(){
  const navigate = useNavigate()
  const [recipename,setrecipename]=useState()
  const [recipedes,setrecipedes]=useState()
  const [recipeimg,setrecipeimg]=useState()
  const url = "https://fad0d70d-d523-442e-8fa3-3fbe1e1b8bf2.mock.pstmn.io/post1"
  let newarr
  // useEffect(() => {
  //   function getRecipe() {
  //     axios
  //       .get("https://fad0d70d-d523-442e-8fa3-3fbe1e1b8bf2.mock.pstmn.io/get1")
  //       .then((response) => {
  //         //JSON.stringify(response.data)
  //         console.log(response.data)
  //         console.log(response.data.recipename)
  //         setrecipename([...response.data.recipename])
  //         setrecipedes([...response.data.recipedes])
  //         setrecipeimg([...response.data.recipeimg])
  //         // console.log(recipeimg)
  //         // newarr=recipeimg.join("")
  //         // console.log(newarr)
  //         // const newdata=[...response.data]
  //         // setrecipelist(newdata)
  //         // setrecipelist([...response.data.recipename])
  //         // console.log(recipelist[0])
  //       })
  //       .catch((error) => {
  //         console.log(error)
  //       })
  //   }
  //   getRecipe()
  // }, [])
  
  /*별점 평가*/
  const [rating, setRating] = useState(0)
  let finalrate
  const handleRating = (rate) => {
    setRating(rate)
  }
  function deleteRate(){
    setRating(0)
  }

  function rateSubmit(e){
    e.preventDefault();
    if(rating==20){
      finalrate=1
    }else if(rating==40){
      finalrate=2
    }else if(rating==60){
      finalrate=3
    }else if(rating==80){
      finalrate=4
    }else if(rating==100){
      finalrate=5
    }else{
      finalrate=0
    }
    console.log("별점평가 값:",finalrate)
    axios.post(url,{
      rate: finalrate
    })
      .then(res=>{
        console.log(res.data)
      })
  }

  return(
    <div className="rs">
      <div className="rs-info">
        <h1>나물비빔밥</h1><br/>
        <p>재료 | 밥, 고추장, 고기 콩나물, 숙주 ,미나리, 계란, 고사리, 도라지, 국간장, 참기름
        </p>
        <p className="rs-recipe">
          레시피 | <br/>
          1. 양지머리로 육수를 낸 후 식혀 기름을 걷어낸 후, 불린 쌀을 넣어 고슬고슬하게 밥을 짓는다.<br/>
          2. 안심은 불고기 양념하여 30분간 재워 국물 없이 구워 한 김 식으면 한입 크기로 자른다.<br/>
          3. 청포묵은 고기와 비슷한 크기로 잘라 끓는 물에 데쳐내고 계란은 노른자와 흰자를 분리해 지단부쳐 곱게 채썬다.<br/>
          4. 콩나물과 숙주, 미나리는 데쳐서 국간장과 참기름으로 간하고, 고사리와 도라지는 참기름을 두른 프라이팬에 살짝 볶아놓는다.<br/>
          5. 밥을 참기름으로 무쳐 그릇에 담고 준비한 재료를 고루 얹는다.<br/>
        </p>
        <p>
          영양성분 | &#40;총 내용량 400g&#41; 580KCAL<br/>
          탄수화물 67G| 단백질 37G| 지방 13G|
        </p>

        <div className='rs-star'>
          이 레시피에 대한 나의 별점<br/>
          <Rating 
            onClick={handleRating} 
            ratingValue={rating} 
            emptyColor="#747474" 
            className="me-2" 
          />
          <button 
            type="button" 
            class="btn btn-outline-secondary me-2" 
            onClick={(e)=>deleteRate()}
          >
            초기화
          </button>
          <button 
            type="button" 
            class="btn btn-outline-danger me-2 " 
            onClick={(e)=>rateSubmit(e)}
          >
            확인
          </button><br/>
          <button 
            class="btn btn-secondary me-2 mt-3" 
            type="button" 
          >
            추천 메뉴 목록 보러가기
          </button>
          <button 
            class="btn btn-secondary mt-3" 
            type="button" 
            onClick={(e)=>navigate("/select")}
          >
            재료 다시 선택하기
          </button>
        </div>
      </div>

      <div className="rs-img">
        <img src="http://file.okdab.com/UserFiles/searching/recipe/000200.jpg"/>
      </div>
    </div>
  )
}
export default Result;