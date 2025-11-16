<?php

declare(strict_types=1);

namespace Src\Products\App\Controllers;

use Illuminate\Container\Attributes\CurrentUser;
use Illuminate\Http\JsonResponse;
use Src\Products\App\Requests\CreateProductRequest;
use Src\Products\App\Resources\ProductResource;
use Src\Products\Domain\Dtos\ProductDto;
use Src\Products\Domain\Model\Product;
use Src\Shared\App\Exceptions\Http\UnauthorizedException;
use Src\Users\Domain\Models\User;

class CreateProductController
{
    public function __invoke(CreateProductRequest $request, #[CurrentUser] User $user): JsonResponse
    {
        $dtos = $request->toDtoArray();
        $products = collect();
        foreach ($dtos as $dto) {
            $product = $this->createProduct($dto, $user);
            $products->push($product);
        }


        return ProductResource::collection($products)->response();
    }

    public function createProduct(ProductDto $dto, User $user): Product
    {
        if (! $user->groups()->where('group_id', $dto->group_id)->exists()) {
            throw new UnauthorizedException();
        }

        return Product::create(
            [
                'name' => $dto->name,
                'amount' => $dto->amount,
                'group_id' => $dto->group_id,
            ]
        );
    }
}
