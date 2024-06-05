import styled from "styled-components";
import ProductionContainer from "./ProductionContainer";
import Navigation from "./Navigation";
import { createGlobalStyle } from "styled-components";
import { Outlet } from "react-router-dom";

const GlobalStyle = createGlobalStyle`
    body{
      background-color: black; 
      color:white;
    }
    `;

function Home({ setUser, user }) {
	return (
		<div>
			<GlobalStyle />
			<Navigation setUser={setUser} />
			{user ? <h1>Welcome, {user.username}</h1> : null}
			<Image />
			<Outlet />
		</div>
	);
}

export default Home;

const Image = styled.img.attrs(() => ({
	src: "https://images.unsplash.com/photo-1518834107812-67b0b7c58434?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1335&q=80",
}))`
    position: absolute;
    z-index:-1;
  `;
