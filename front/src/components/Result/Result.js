import React, { useState, useEffect } from "react"
import axios from "axios"
import "../../index.css"

function Result(){
  const [recipename,setrecipename]=useState()
  const [recipedes,setrecipedes]=useState()
  const [recipeimg,setrecipeimg]=useState()
  let newarr
  useEffect(() => {
    function getRecipe() {
      axios
        .get("https://fad0d70d-d523-442e-8fa3-3fbe1e1b8bf2.mock.pstmn.io/get1")
        .then((response) => {
          //JSON.stringify(response.data)
          console.log(response.data)
          console.log(response.data.recipename)
          setrecipename([...response.data.recipename])
          setrecipedes([...response.data.recipedes])
          setrecipeimg([...response.data.recipeimg])
          // console.log(recipeimg)
          // newarr=recipeimg.join("")
          // console.log(newarr)
          // const newdata=[...response.data]
          // setrecipelist(newdata)
          // setrecipelist([...response.data.recipename])
          // console.log(recipelist[0])
        })
        .catch((error) => {
          console.log(error)
        })
    }
    getRecipe()
  }, [])
 

  return(
    <div class="container-fluid">
      <div class="row">
        <div class="col-md-7" style={{backgroundColor:"#E9DCCD"}}>
          <h1>{recipename}</h1>
          영양성분 |<br/>
          {recipedes}<br/>

            <button class="btn btn-secondary" type="button">다른 추천 메뉴 보러가기</button><br/>
            <button class="btn btn-secondary" type="button">오늘의 메뉴로 선택</button>
        </div>


        <div class="col-md-5" style={{backgroundColor:"#A8BA88"}}>
          <img src="https://recipe1.ezmember.co.kr/cache/recipe/2020/09/30/e81f37d07d0d3fbe3fb7aa12ede4f5ff1.jpg" height="800"/>
        </div>
      </div>
    </div>
  )
}
export default Result;