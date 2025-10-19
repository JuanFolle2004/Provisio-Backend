<?php

declare(strict_types=1);

namespace Controllers;

use Illuminate\Container\Attributes\CurrentUser;
use Illuminate\Http\JsonResponse;
use Src\Products\Domain\Model\Product;
use Src\Shared\App\Exceptions\Http\UnauthorizedException;
use Src\Users\Domain\Models\User;

class DeleteProductController
{
    public function __invoke(Product $product, #[CurrentUser] User $user): JsonResponse
    {
        if (! $user->groups()->where('group_id', $product->group_id)->exists()) {
            throw new UnauthorizedException();
        }
        $product->delete();

        return response()->json();
    }
}
