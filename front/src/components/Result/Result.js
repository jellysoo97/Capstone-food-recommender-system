import React, { useState } from "react"
import { useParams, useNavigate } from "react-router-dom"
import axios from "axios"
import { Rating } from "react-simple-star-rating"
import "../../index.css"

function Result() {
  const navigate = useNavigate()
  let cate = useParams()
  const starpost = `http://localhost:8000/preference/last`
  let user_idx = window.localStorage.getItem("idx")

  // 최종 메뉴 결과 받아오기(메뉴이름,이미지,시간,난이도,양)
  // 제일 적합한 것으로 추천된 메뉴의 id를 로컬스토리지 "selectmenuid"에 저장함
  let rsmenuid = parseInt(window.localStorage.getItem("selectmenuid"))
  let rsmenu_raw = JSON.parse(window.localStorage.getItem("result"))
  let rsmenu = rsmenu_raw[rsmenuid]
  let rsname = rsmenu.basic_info.recipe_nm_ko
  let rsimg = rsmenu.basic_info.img_url
  let rstime = rsmenu.basic_info.cooking_time
  let rslv = rsmenu.basic_info.level_nm
  let rsqnt = rsmenu.basic_info.qnt
  //레시피 정보
  let rsrecipe = []
  for (let i = 0; i < rsmenu.order_info.length; i++) {
    rsrecipe.push({
      reid: rsmenu.order_info[i].cooking_no,
      reinfo: rsmenu.order_info[i].cooking_dc,
    })
  }
  function RecipeList(props) {
    let recipeid = props.recipe.reid
    let recipe = props.recipe.reinfo
    return (
      <div>
        {recipeid} . {recipe}
        <br />
      </div>
    )
  }

  // 레시피 재료정보
  let rswhat = ""
  for (let i = 0; i < rsmenu.what_info.length; i++) {
    if (i == rsmenu.what_info.length - 1) {
      rswhat =
        rswhat + rsmenu.what_info[i].irdnt_nm + rsmenu.what_info[i].irdnt_cpcty
    } else {
      rswhat =
        rswhat +
        rsmenu.what_info[i].irdnt_nm +
        rsmenu.what_info[i].irdnt_cpcty +
        ","
    }
  }

  /*별점 평가*/
  const [rating, setRating] = useState(0)
  let finalrate
  const handleRating = (rate) => {
    setRating(rate)
  }
  function deleteRate() {
    setRating(0)
  }

  function rateSubmit(e) {
    e.preventDefault()
    if (rating == 20) {
      finalrate = 1
    } else if (rating == 40) {
      finalrate = 2
    } else if (rating == 60) {
      finalrate = 3
    } else if (rating == 80) {
      finalrate = 4
    } else if (rating == 100) {
      finalrate = 5
    } else {
      finalrate = 0
    }

    console.log("별점평가 값:", finalrate)
    axios
      .post(starpost, {
        user_id: parseInt(user_idx),
        recipe_id: parseInt(rsmenu.order_info[0].recipe_id),
        ratings: parseFloat(finalrate),
      })
      .then((res) => {
        console.log(res.data)
        alert("별점이 저장되었습니다.")
      })
  }

  // 레시피 영양성분
  let rsingre = rsmenu.ingre_info[0]
  let rskcal = rsingre.energy //Kcal
  let rspro = rsingre.protein //단백질
  let rsfat = rsingre.fat //지방
  let rscar = rsingre.carbo //탄수화물
  let rsna = rsingre.natrium //나트륨
  let rsfi = rsingre.fiber //식이섬유
  let rscalci = rsingre.calcium //칼슘
  let rsst = rsingre.steel // 철

  return (
    <div className="rs">
      <div className="rs-info">
        <h1>{rsname}</h1>
        <p>
          <span>조리시간 | </span>
          {rstime} ,<span> 레시피 난이도 | </span>
          {rslv} ,<span> {rsqnt}</span> <br />
          <span>재료 | </span>
          {rswhat}
          <br />
        </p>
        <p className="rs-recipe">
          <span>레시피 |</span>
          {rsrecipe.map((re, index) => (
            <RecipeList recipe={re} key={index} />
          ))}
        </p>
        <p>
          <span>칼로리 | </span> {rskcal} kcal
          <br />
          <span>영양성분 | </span>
          <br />
          탄수화물 | {rscar}g &#40;식이섬유 {rsfi}g&#41;, 단백질 | {rspro}g
          &#40;칼슘 {rscalci}mg, 철 {rsst}mg&#41;, 지방 | {rsfat}g, 나트륨 |{" "}
          {rsna}g
        </p>
        <div className="rs-star">
          <span>이 레시피에 대한 나의 별점</span>
          <br />
          <Rating
            onClick={handleRating}
            ratingValue={rating}
            emptyColor="#747474"
            className="me-2"
          />
          <button
            type="button"
            className="btn btn-outline-secondary me-2"
            onClick={(e) => deleteRate()}
          >
            초기화
          </button>
          <button
            type="button"
            className="btn btn-outline-danger me-2 "
            onClick={(e) => rateSubmit(e)}
          >
            확인
          </button>
          <br />
          <button
            className="btn btn-secondary me-2 mt-3"
            type="button"
            onClick={(e) => navigate(`/resultlist/${cate.cate}`)}
          >
            추천 메뉴 목록 보러가기
          </button>
          <button
            className="btn btn-secondary mt-3"
            type="button"
            onClick={(e) => navigate(`/select/${cate.cate}`)}
          >
            재료 다시 선택하기
          </button>
        </div>
      </div>

      <div className="rs-img">
        <img src={rsimg} />
      </div>
    </div>
  )
}
export default Result
