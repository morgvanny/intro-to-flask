import { useEffect, useState } from "react";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import Home from "./components/Home";
import Signup from "./components/Signup";
import Login from "./components/Login";
import ProductionDetail from "./components/ProductionDetail";
import ProductionForm from "./components/ProductionForm";
import ProductionContainer from "./components/ProductionContainer";

function App() {
	const [productions, setProductions] = useState([]);
	const [user, setUser] = useState();

	useEffect(() => {
		fetch("/api/me").then((r) => {
			if (r.ok) {
				return r.json().then(setUser);
			}
			setUser(null);
		});

		fetchProductions();
	}, []);

	const fetchProductions = () =>
		fetch("/api/productions")
			.then((res) => {
				if (res.ok) {
					return res.json();
				}
			})
			.then(setProductions);

	const addProduction = (production) =>
		setProductions((current) => [...current, production]);

	const router = createBrowserRouter([
		{
			path: "/",
			element: <Home user={user} setUser={setUser} />,
			children: [
				{
					path: "/login",
					element: <Login user={user} setUser={setUser} />,
				},
				{
					path: "/signup",
					element: <Signup user={user} setUser={setUser} />,
				},
				{
					path: "/productions/new",
					element: <ProductionForm addProduction={addProduction} />,
				},
				{
					path: "/",
					element: (
						<ProductionContainer user={user} productions={productions} />
					),
				},
				{
					path: "/productions/:id",
					element: <ProductionDetail />,
				},
			],
		},
	]);

	return <RouterProvider router={router} />;
}

export default App;
