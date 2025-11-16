<?php

declare(strict_types=1);

namespace Src\Products\App\Resources;

use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;
use Src\Products\Domain\Model\Product;

/**
 * @mixin Product
 */
class ProductResource extends JsonResource
{
    public function toArray(Request $request): array
    {
        return [
            'name' => $this->name,
            'amount' => $this->amount];
    }
}
