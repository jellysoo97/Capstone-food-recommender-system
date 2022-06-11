import React, { useState, useEffect } from "react"
import { useParams, useNavigate } from "react-router-dom"
import axios from "axios"
import "../../index.css"
function ResultList(){
  const navigate = useNavigate()
  let cate = useParams()

  function SetSelMenu(e){
    window.localStorage.setItem("selectmenuid",e.target.id)
    navigate(`/result/${cate.cate}`)
  }

  function Menulist(props){
    let menu = props.menu
    return(
      <button type="button" class="list-group-item list-group-item-action list-group-item-light" id={menu.id}
      onClick={(e)=>SetSelMenu(e)}>
        <img src={menu.url} id={menu.id} onClick={(e)=>SetSelMenu(e)}/><br/><br/>
        {menu.name}
      </button>
    )
  }

  let user = window.localStorage.getItem("userId")
  let resultdata=window.localStorage.getItem('result')
  resultdata= JSON.parse(resultdata)
  let resultindex= []
  for (let x in resultdata){
    resultindex.push(x)
  }
  let resultmenu = []
  let resultmenu2 = []
  for (let i=0;i<resultindex.length;i++){
    if(i<5){
      resultmenu.push({
      "id": resultindex[i],
      "name":resultdata[resultindex[i]].basic_info.recipe_nm_ko,
      "url":resultdata[resultindex[i]].basic_info.img_url,
      })    
    }else{
      resultmenu2.push({
        "id": resultindex[i],
        "name":resultdata[resultindex[i]].basic_info.recipe_nm_ko,
        "url":resultdata[resultindex[i]].basic_info.img_url,
      }) 
    }
  }


  return(
    <div className='rl'>
      <div className='rl-list'>
        <h2>{user}님에게 추천하는 메뉴</h2>
        <h5>메뉴를 눌러 해당 레시피로 이동하세요!</h5>
        <div className="list-group list-group-horizontal">
          {resultmenu.map((me, index) => (
          <Menulist menu={me} key={index} />
          ))}
        </div>
        <div className="list-group list-group-horizontal">
          {resultmenu2? resultmenu2.map((me, index) => (
          <Menulist menu={me} key={index} />
          )):""}
        </div>
      </div>
    </div>
  )
}
export default ResultList;