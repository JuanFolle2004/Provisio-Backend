<?php

declare(strict_types=1);

use Illuminate\Support\Facades\Route;
use Src\Shared\App\Exceptions\Http\InvalidActionException;

Route::get('invalid', static fn() => throw new InvalidActionException("Is not valid"));

Route::get('/', static fn(): \Illuminate\Contracts\View\View|\Illuminate\Contracts\View\Factory => view('welcome'));

Route::get('/login', static fn(): \Illuminate\Contracts\View\View|\Illuminate\Contracts\View\Factory => view('welcome'))->name('login');


