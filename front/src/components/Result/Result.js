import React, { useState, useEffect } from "react"
import axios from "axios"
import "../../index.css"

function Result(){
  const [recipename,setrecipename]=useState()
  const [recipedes,setrecipedes]=useState()
  const [recipeimg,setrecipeimg]=useState()
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
 

  return(
    <div className="rs">
      <div className="rs-info">
        <h1>음식 이름</h1><br/>
        <p>영양성분 | &#40;총 내용량 400g&#41; 450KCAL<br/>
          탄수화물 67G| 단백질 37G| 지방 13G|
        </p><br/>
        <div className="rs-btn">
          <button 
            class="btn btn-secondary" 
            type="button" 
            style={{marginRight: "10px"}}
          >
            다른 추천 메뉴 보러가기
          </button>
          <button 
            class="btn btn-secondary" 
            type="button"
          >
            오늘의 메뉴로 선택
          </button>
        </div>
      </div>
      <div className="rs-img">
        <h2>음식 사진</h2>
      </div>
    </div>
  )
}
export default Result;