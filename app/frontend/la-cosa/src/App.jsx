
import { BrowserRouter, Route,Routes } from 'react-router-dom'
import './App.css'
import PageCreateGame from './pages/PageCreateGame'
import PageHome from './pages/PageHome'
import PageJoinGame from './pages/PageJoinGame'
import PageWaitingRoom from './pages/PageWaitingRoom'
import PageGame from './pages/PageGame'
import PageGameResult from './pages/PageGameResult'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path='/' element={<PageHome></PageHome>}></Route>
        <Route path='/crearpartida' element={<PageCreateGame></PageCreateGame>}></Route>
        <Route path='/unirsepartida' element={<PageJoinGame></PageJoinGame>}></Route>
        <Route path='/saladeespera' element={<PageWaitingRoom></PageWaitingRoom>}>
        </Route>
        <Route path='/juego' element={<PageGame></PageGame>}>
        </Route>
        <Route path="/resultados/:gameID" element={<PageGameResult gameID={sessionStorage.getItem("id_game")}></PageGameResult>}></Route>
      </Routes>
    </BrowserRouter>
  )

}

export default App;
