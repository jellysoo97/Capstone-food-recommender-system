import React, { Suspense } from "react"
import { Routes, Route } from "react-router-dom"

import NavBar from "./components/Common/NavBar"
import Footer from "./components/Common/Footer"

import LandingPage from "./components/LandingPage"
import Signup from "./components/Auth/Signup"
import Login from "./components/Auth/Login"
import Select from "./components/Select/Select"
import Result from "./components/Result/Result"
import ResultList from "./components/Result/ResultList"
import FirstPrefer from "./components/Auth/FirstPrefer"

function App() {
  return (
    <Suspense
      fallback={
        <div class="d-flex justify-content-center">
          <div className="spinner-border text-success" role="status">
            <span className="visually-hidden">Loading...</span>
          </div>
        </div>
      }
    >
      <NavBar />
      <div style={{ minHeight: "calc(100vh - 80px)" }}>
        <Routes>
          <Route exact path="/" element={<LandingPage />} />
          <Route exact path="/signup" element={<Signup />} />
          <Route exact path="/prefer" element={<FirstPrefer />} />
          <Route exact path="/login" element={<Login />} />
          <Route exact path="/select/:cate" element={<Select />} />
          <Route exact path="/result/:cate" element={<Result />} />
          <Route exact path="/resultlist/:cate" element={<ResultList />} />
        </Routes>
      </div>
      <Footer />
    </Suspense>
  )
}
export default App
