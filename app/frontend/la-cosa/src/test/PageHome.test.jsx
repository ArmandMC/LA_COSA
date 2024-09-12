import '@testing-library/jest-dom';
import React from 'react';
import { render, screen } from '@testing-library/react';
import PageHome from '../pages/PageHome';

describe('PageHome Component', () => {
  test('Renderiza sin errores', () => {
    render(<PageHome />);
    expect(screen.getByText('LA COSA')).toBeInTheDocument();
  });

  test('Muestra el boton "Crear Partida"', () => {
    render(<PageHome />);
    expect(screen.getByText('Crear Partida')).toBeInTheDocument();
  });

  test('Muestra el botón "Unir Partida" como deshabilitado cuando no se selecciona ninguna partida', () => {
    render(<PageHome />);
    const unirPartidaButton = screen.getByText('Unir Partida');
    expect(unirPartidaButton).toBeInTheDocument();
    expect(unirPartidaButton).toHaveAttribute('aria-disabled', 'true');
  });
});
