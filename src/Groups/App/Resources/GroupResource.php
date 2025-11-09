<?php

declare(strict_types=1);

namespace Src\Groups\App\Resources;

use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;
use Src\Groups\Domain\Model\Group;

/**
 * @mixin Group
 */
class GroupResource extends JsonResource
{
    public function toArray(Request $request): array
    {
        return [
            'id' => $this->id,
            'name' => $this->name,
            'assignments_count' =>$this->whenLoaded('assignments')->count(),
            'products_count' => $this->whenLoaded('products')->count(),
            'users_count' => $this->whenLoaded('users')->count(),
        ];
    }
}
