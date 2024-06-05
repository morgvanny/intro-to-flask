import { useState } from "react";
import { GiHamburgerMenu } from "react-icons/gi";
import { Link } from "react-router-dom";
import styled from "styled-components";

function Navigation({ setUser }) {
	const [menu, setMenu] = useState(false);

	const handleLogout = () => {
		fetch("/api/sign_out", {
			method: "DELETE",
		}).then((res) => {
			if (res.ok) {
				setUser(null);
			}
		});
	};

	return (
		<Nav>
			<NavH1>Flatiron Theater Company</NavH1>
			<Menu>
				{!menu ? (
					<div onClick={() => setMenu(!menu)}>
						<GiHamburgerMenu size={30} />
					</div>
				) : (
					<ul>
						<li onClick={() => setMenu(!menu)}>x</li>
						<li>
							<Link to="/productions/new">New Production</Link>
						</li>
						<li>
							<Link to="/"> Home</Link>
						</li>
						<li>
							<Link to="/login"> Login</Link>
						</li>
						<li>
							<Link to="/signup"> Signup</Link>
						</li>
						<li>
							<button type="button" onClick={handleLogout}>
								Logout
							</button>
						</li>
					</ul>
				)}
			</Menu>
		</Nav>
	);
}

export default Navigation;

const NavH1 = styled.h1`
  font-family: "Splash", cursive;
`;
const Nav = styled.div`
  display: flex;
  justify-content: space-between;
`;

const Menu = styled.div`
  display: flex;
  align-items: center;
  a {
    text-decoration: none;
    color: white;
    font-family: Arial;
  }
  a:hover {
    color: pink;
  }
  ul {
    list-style: none;
  }
`;
