<?php

declare(strict_types=1);



use Illuminate\Container\Attributes\CurrentUser;
use Illuminate\Support\Facades\Route;
use Src\Users\App\Controllers\{GetUserController, DeleteUserController, ListUserController, SignUpController, UpdateUserController,LoginController};
use Src\Assignment\App\Controllers\AssignProductController;
use Src\Assignment\App\Controllers\DeleteAssignmentController;
use Src\Assignment\App\Controllers\GetAssignmentController;
use Src\Assignment\App\Controllers\PatchAssignmentController;
use Src\Groups\App\Controllers\GetGroupController;
use Src\Groups\App\Controllers\ListGroupsController;
use Src\Groups\App\Controllers\UpsertGroupController;
use Src\Products\App\Controllers\ListProductController;


/*
|--------------------------------------------------------------------------
| API Routes
|--------------------------------------------------------------------------
|
| Here is where you can register API routes for your application. These
| routes are loaded by the RouteServiceProvider and all of them will
| be assigned to the "api" middleware group. Make something great!
|
*/

Route::middleware('auth:api')
    ->get('/me', function (#[CurrentUser] $user) {
        return response()->json([
            'data' => $user,
        ]);
    });

/*
|--------------------------------------------------------------------------
| Users Routes
|--------------------------------------------------------------------------
*/
Route::prefix('users')
    ->middleware([])
    ->group(static function (): void {
        Route::get('/', ListUserController::class);
        Route::get('/{user}', GetUserController::class)
            ->withTrashed()
            ->whereNumber('user');
        Route::post('/', SignUpController::class);
        Route::put('/{user}', UpdateUserController::class)
            ->whereNumber('user');
        Route::delete('/{user}', DeleteUserController::class)
            ->whereNumber('user');
        Route::post('/login', LoginController::class);
    });

Route::prefix('assignments')
    ->middleware(['auth:api'])
    ->group(static function (): void {
        Route::get('/{assignment}',GetAssignmentController::class);
        Route::delete('/{assignment}',DeleteAssignmentController::class);
        Route::patch('/',PatchAssignmentController::class);
        Route::post('/assign', AssignProductController::class);
    });

Route::prefix('groups')
    ->middleware(['auth:api'])
    ->group(static function (): void {
        Route::get('/{group}', GetGroupController::class);
        Route::post('/',UpsertGroupController::class);
        Route::get('/',ListGroupsController::class);
    });

Route::prefix('products')
    ->middleware(['auth:api'])
    ->group(static function (): void {
        Route::get('/{group}',ListProductController::class);
    });
